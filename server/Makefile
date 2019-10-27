MDIR=afd/

MODEL=$(MDIR)afdmodel.ckpt.data-00000-of-00001

.PHONY: frag-model defrag-model test

frag-model:
	split -b90m $(MODEL) && mv x?* $(MDIR) && $(RM) $(MODEL)

defrag-model:
	cat $(MDIR)x?* > $(MODEL) && $(RM) $(MDIR)x?*

test:
	python test_api.py
