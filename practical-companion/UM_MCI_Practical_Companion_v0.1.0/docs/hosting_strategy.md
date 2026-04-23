# Hosting and release strategy

## Recommended publication split

### Zenodo
Publish the **semantic core** on Zenodo:
- stable ontology,
- Compass seed,
- defaults,
- edge-family seed,
- record/context schemas,
- minimal semantic documentation.

Zenodo should be the **canonical citable source** for the stable core release.

### GitHub
Use GitHub for the faster-moving practical layer:
- practical companion examples,
- projection compiler,
- retrospective extraction tools,
- signature libraries,
- implementation references,
- empirical audit workflows.

## Should the GitHub repository also contain the core?

Yes—often that is the easiest arrangement for users.

A good public GitHub repository may contain:
- a **read-only mirror** or pinned snapshot of the Zenodo core release, and
- the faster-moving practical companion materials.

That gives users a one-stop workspace while preserving a clean release boundary:
- **cite Zenodo** for the stable core release,
- **use GitHub** for practical workflows and faster iteration.

## Important Zenodo/GitHub integration note

If you enable a GitHub repository for Zenodo integration, Zenodo archives **releases from that repository**. It does not automatically ingest a practical-companion release into an unrelated pre-existing core DOI.

So if you want the core DOI to remain a separate citable object, you should either:
- keep the core as its own Zenodo-managed release and treat GitHub as a mirror/workspace, or
- separate the core and companion into different repositories or release channels.

## Recommended layout

```text
um-mci/
  core_snapshot/
    UM_MetaControl_Interface_Core_Semantic_Package_v0.1.0/
  companion/
    ...practical companion materials...
```

A lighter alternative is to keep the core unpacked as a sibling directory and point tools to it via `--core-root`.

## What to do with the nine theoretical framework frameworks

Do **not** make the machine-readable core or the practical companion depend on embedded copies of the theory PDFs.

Instead:
- keep the canonical theoretical framework documents on Zenodo,
- link to them from both the core and the practical companion,
- optionally mirror them on GitHub only as convenience copies if you really want to, but treat Zenodo as the source of truth for citation and stable access.

This keeps the software-facing packages smaller and avoids duplicate maintenance of theory artifacts that already have their own stable record pages.

## Theory PDFs on GitHub

You may keep convenience copies or mirrors of the theoretical framework PDFs on GitHub if that genuinely helps users, but treat the Zenodo records as the canonical citation source. Do not mint a second DOI for the same theory artifact; instead, point users back to the existing Zenodo record.


## If you archive the practical companion itself

If you later archive the practical companion through Zenodo, treat it as a **separate Zenodo object** unless you intentionally want to version the same object as the core (which is usually not recommended because the roles differ). A GitHub release of the practical companion will not automatically become a new version of an unrelated pre-existing core DOI.


## Community accumulation

A public GitHub repository may accumulate cross-domain worked examples, retrospective cases, signature seeds, and candidate route-prior notes **as long as they continue to write against the stable public IDs from the Zenodo core**. This is exactly the point of keeping the core stable and the practical layer revisable.
