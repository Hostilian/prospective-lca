"""Bundle the verified review exports and pin their source revision."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools.verify_review_package import verify_package

FILES = ("index.html", "customer/index.html", "reviewer/index.html", "report.html",
         "run.json", "manifest.json", "results.csv", "contributions.csv", "assumptions.csv",
         "review-diagnostics.json", "preview-manifest.json")


def package_review(package, source_ref, output):
    if not re.fullmatch(r"[0-9a-f]{40}", source_ref):
        raise ValueError("Source revision must be a full commit SHA")
    verify_package(package)
    members = {name: (package / name).read_bytes() for name in FILES}
    source_url = f"https://github.com/Hostilian/prospective-lca/tree/{source_ref}"
    members["REVIEW-README.md"] = f"""# Prospective LCA: technical review package

Open reviewer/index.html for the technical report or customer/index.html for the study brief.
Keep the folders and data files together so navigation and optional downloads work.
Core report content works offline without JavaScript.

Synthetic demonstration only; no scientific acceptance or AWAM endorsement.
The supplied display values are preserved separately from full-precision calculations.

Source revision: {source_ref}
[Source, tests, review guide and professional-context research]({source_url})

From that exact source checkout:
python tools/verify_review_package.py --package <unpacked-package-directory>

SHA256SUMS verifies the packaged file bytes. It does not certify the science or authorship.
The source repository's internal-use notice applies; licence/IP terms remain unresolved.
""".encode("utf-8")
    members["review-snapshot.json"] = (json.dumps({"source_revision": source_ref,
        "source_url": source_url, "scientific_approval": False,
        "document_version": json.loads(members["preview-manifest.json"])["document_version"]}, indent=2) + "\n").encode("utf-8")
    members["SHA256SUMS"] = ("\n".join(f"{hashlib.sha256(content).hexdigest()}  {name}" for name, content in sorted(members.items())) + "\n").encode("utf-8")
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w") as archive:
        for name, content in sorted(members.items()):
            item = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            item.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(item, content)
    with zipfile.ZipFile(output) as archive:
        for name, content in members.items():
            if archive.read(name) != content:
                raise ValueError(f"Archive round-trip mismatch: {name}")
    fingerprint = hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix + ".sha256").write_text(f"{fingerprint}  {output.name}\n", encoding="utf-8", newline="\n")
    return {"archive": str(output), "sha256": fingerprint, "source_revision": source_ref}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--source-ref", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(package_review(args.package, args.source_ref, args.out), indent=2))
