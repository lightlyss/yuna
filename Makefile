MDIR=server/afd/

MODEL=$(MDIR)afdmodel.ckpt.data-00000-of-00001

.PHONY: frag-model defrag-model

frag-model:
	split -b90m $(MODEL) && mv x?* $(MDIR) && $(RM) $(MODEL)

defrag-model:
	cat $(MDIR)x?* > $(MODEL) && $(RM) $(MDIR)x?*
