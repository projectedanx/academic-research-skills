Instability: Loose dependency versioning in `requirements-dev.txt` allowed unpinned, floating packages (`>=` and unversioned packages), exposing the pipeline to upstream regressions. No root-level trash scripts were found.
Fortification: Enforced strict semantic version pinning (`==`) across all development dependencies in `requirements-dev.txt` to guarantee deterministic builds.
