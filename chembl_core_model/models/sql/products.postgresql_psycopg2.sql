create extension if not exists "rdkit";

select distinct c.molregno,
                mol_from_ctab(molfile::cstring) ctab into compound_mols
from compound_structures c,
     molecule_hierarchy h
where is_valid_ctab(molfile::cstring) and
      c.molregno=h.parent_molregno;

create index rdkit_mol_idx on compound_mols using gist(ctab);

select molregno,torsionbv_fp(ctab) as torsionbv,morganbv_fp(ctab,2) as mfp2,featmorganbv_fp(ctab,2) as ffp2 into fps_rdkit from compound_mols;

select molregno, torsionbv_fp(ctab) as torsionbv, morganbv_fp(ctab,2) as mfp2, featmorganbv_fp(ctab,2) as ffp2, rdkit_fp(ctab) as rdkfp, atompairbv_fp(ctab) as atombv, layered_fp(ctab) as layeredfp, maccs_fp(ctab) as maccsfp into fps2_rdkit from compound_mols;

create index fps_ttbv_idx on fps_rdkit using gist(torsionbv);
create index fps_mfp2_idx on fps_rdkit using gist(mfp2);
create index fps_ffp2_idx on fps_rdkit using gist(ffp2);

create index fps2_ttbv_idx on fps2_rdkit using gist(torsionbv);
create index fps2_mfp2_idx on fps2_rdkit using gist(mfp2);
create index fps2_ffp2_idx on fps2_rdkit using gist(ffp2);
create index fps2_rdkfp_idx on fps2_rdkit using gist(rdkfp);
create index fps2_atombv_idx on fps2_rdkit using gist(atombv);
create index fps2_layfp_idx on fps2_rdkit using gist(layeredfp);
create index fps2_maccsfp_idx on fps2_rdkit using gist(maccsfp);

alter table compound_mols add primary key (molregno);
alter table fps_rdkit add primary key (molregno);
alter table fps2_rdkit add primary key (molregno);