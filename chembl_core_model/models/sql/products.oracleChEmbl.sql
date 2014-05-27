------------------------------------------------------------------------------------------------------------------------
 CREATE SEQUENCE chembl_id_sq
 START WITH 1
 INCREMENT BY 1;

;
------------------------------------------------------------------------------------------------------------------------

create or replace trigger "DOCS_TR"
BEFORE INSERT ON "DOCS"
REFERENCING NEW AS New OLD AS Old
FOR EACH ROW


BEGIN

   if(:NEW.chembl_id is null) then :NEW.chembl_id := 'CHEMBL' || chembl_id_sq.nextval;--
   end if;--

   if(:NEW.doc_id is null) then :NEW.doc_id := docs_sq.nextval;--
   end if;--

   INSERT INTO chembl_id_lookup (chembl_id, entity_type, entity_id)
   VALUES (:NEW.chembl_id, 'DOCUMENT', :NEW.doc_id);--

   EXCEPTION
     WHEN OTHERS THEN
       -- Consider logging the error and then re-raise
       RAISE;--

    END;--

;
------------------------------------------------------------------------------------------------------------------------

create or replace trigger "MOLECULE_DICTIONARY_TR"
BEFORE INSERT ON "MOLECULE_DICTIONARY"
REFERENCING NEW AS New OLD AS Old
FOR EACH ROW


BEGIN
  IF (:NEW.chembl_id IS NULL OR :NEW.chembl_id = '')
  THEN
     :NEW.chembl_id := 'CHEMBL' || chembl_id_sq.NEXTVAL;--
  END IF;--

  IF (:NEW.molregno IS NULL)
  THEN
     :NEW.molregno := molecule_dictionary_sq.NEXTVAL;--
  END IF;--

  INSERT INTO chembl_id_lookup (chembl_id, entity_type, entity_id)
    VALUES   (:NEW.chembl_id, 'COMPOUND', :NEW.molregno);--
EXCEPTION
  WHEN OTHERS
  THEN
     -- Consider logging the error and then re-raise
     RAISE;--
    END;--

;
------------------------------------------------------------------------------------------------------------------------

create or replace trigger "ASSAYS_TR"
BEFORE INSERT ON "ASSAYS"
REFERENCING NEW AS New OLD AS Old
FOR EACH ROW


BEGIN
   if(:NEW.assay_id is null) then :NEW.assay_id := assays_sq.nextval;--
   end if;--

   if(:NEW.chembl_id is null) then :NEW.chembl_id := 'CHEMBL' || chembl_id_sq.nextval;--
   end if;--

   INSERT INTO chembl_id_lookup (chembl_id, entity_type, entity_id)
   VALUES (:NEW.chembl_id, 'ASSAY', :NEW.assay_id);--

   EXCEPTION
     WHEN OTHERS THEN
       -- Consider logging the error and then re-raise
       RAISE;--

    END;--
;
------------------------------------------------------------------------------------------------------------------------

create or replace trigger "TARGET_DICTIONARY_TR"
BEFORE INSERT ON "TARGET_DICTIONARY"
REFERENCING NEW AS New OLD AS Old
FOR EACH ROW


BEGIN
   if(:NEW.tid is null) then :NEW.tid := TARGET_DICTIONARY_SQ.nextval;--
   end if;--

   if(:NEW.chembl_id is null) then :NEW.chembl_id := 'CHEMBL' || chembl_id_sq.nextval;--
   end if;--

   INSERT INTO chembl_id_lookup (chembl_id, entity_type, entity_id)
   VALUES (:NEW.chembl_id, 'TARGET', :NEW.tid);--

   EXCEPTION
     WHEN OTHERS THEN
       -- Consider logging the error and then re-raise
       RAISE;--
    END;--
;
------------------------------------------------------------------------------------------------------------------------

create or replace trigger "CMPD_STR_UPDATE_TRIG"
BEFORE UPDATE
ON COMPOUND_STRUCTURES
REFERENCING NEW AS New OLD AS Old
FOR EACH ROW

BEGIN

   if(:NEW.molfile is null and :OLD.molfile is not null)
   then RAISE_APPLICATION_ERROR(-20100, 'Delete molfile: operation not permitted');--
   end if;--

   if((:NEW.standard_inchi is null and :OLD.standard_inchi is not null) or (:NEW.standard_inchi <> :OLD.standard_inchi))
   then RAISE_APPLICATION_ERROR(-20100, 'Delete or update standard_inchi: operation not permitted');--
   end if;--

   if((:NEW.standard_inchi_key is null and :OLD.standard_inchi_key is not null) or (:NEW.standard_inchi_key <> :OLD.standard_inchi_key))
   then RAISE_APPLICATION_ERROR(-20100, 'Delete or update standard_inchi_key: operation not permitted');--
   end if;--

   if(dbms_lob.compare(:NEW.molfile, :OLD.molfile) <> 0)
   then
   :NEW.canonical_smiles := null;--

   update molecule_dictionary set molfile_update = sysdate where molregno = :NEW.molregno;
   delete from compound_properties where molregno = :NEW.molregno;
   insert into compound_properties (molregno) values (:NEW.molregno);
   delete from compound_images where molregno = :NEW.molregno;
   update compound_mols set ctab = mol(:NEW.molfile) where molregno = :NEW.molregno;

   end if;--


   EXCEPTION
     WHEN OTHERS THEN
       -- Consider logging the error and then re-raise
       RAISE;--
END;--
;

------------------------------------------------------------------------------------------------------------------------

create or replace trigger "COMPOUND_STRUCT_TRIG"
AFTER INSERT ON "COMPOUND_STRUCTURES"
REFERENCING NEW AS New OLD AS Old
FOR EACH ROW

BEGIN

   INSERT INTO compound_properties (molregno)
   VALUES (:NEW.molregno);--

   INSERT INTO compound_mols (molregno, ctab) values (:NEW.molregno, mol(:NEW.molfile));

END;--

------------------------------------------------------------------------------------------------------------------------