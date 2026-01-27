import json
import subprocess
import sys

"""
Generate a CycloneDX SBOM (JSON) for the project.
Requires `cyclonedx-bom` installed (see requirements-dev.txt).
"""

def main():
    try:
        subprocess.check_call([sys.executable, '-m', 'cyclonedx_bom', '--format', 'json', '--output', 'sbom.json'])
        print('[SBOM] Generated sbom.json')
    except subprocess.CalledProcessError as e:
        print(f'[SBOM] Failed: {e}')
        sys.exit(1)

if __name__ == '__main__':
    main()
