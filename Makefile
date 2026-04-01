PROJECT_ROOT := $(shell pwd)

.PHONY: install preprocess nprint csv train test help

help:
	@echo "OsirisML - Passive OS Fingerprinting"
	@echo ""
	@echo "Setup:"
	@echo "  make install              Install nprint and Python dependencies (requires sudo)"
	@echo ""
	@echo "Preprocessing (full pipeline from raw .pcap):"
	@echo "  make preprocess PCAP=file.pcap   Run full pipeline: tcpdump -> nprint -> csv"
	@echo ""
	@echo "Preprocessing (individual steps):"
	@echo "  make nprint               Convert pcap files in data/pcap/pcap_os_split/ to .npt"
	@echo "  make csv CSV=output.csv   Convert .npt files to a single labeled CSV"
	@echo ""
	@echo "Model:"
	@echo "  make train CSV=file.csv MODEL=name.json           Train a new XGBoost model"
	@echo "  make test MODEL=model.json CSV=file.csv           Test with an existing model"
	@echo "  make tune CSV=file.csv                            Run hyperparameter tuning"

install:
	sudo $(PROJECT_ROOT)/configure/configure.sh

preprocess:
ifndef PCAP
	$(error PCAP is required. Usage: make preprocess PCAP=file.pcap)
endif
	cd $(PROJECT_ROOT)/preprocessing && ./process_pcap.sh $(PCAP)

nprint:
	cd $(PROJECT_ROOT)/preprocessing && ./nprint.sh

csv:
ifndef CSV
	$(error CSV is required. Usage: make csv CSV=output.csv)
endif
	cd $(PROJECT_ROOT)/preprocessing && python3 npt_to_csv.py $(CSV)

train:
ifndef CSV
	$(error CSV is required. Usage: make train CSV=file.csv MODEL=name.json)
endif
ifndef MODEL
	$(error MODEL is required. Usage: make train CSV=file.csv MODEL=name.json)
endif
	cd $(PROJECT_ROOT)/model && python3 xgboostmodel.py $(CSV) $(MODEL)

test:
ifndef MODEL
	$(error MODEL is required. Usage: make test MODEL=model.json CSV=file.csv)
endif
ifndef CSV
	$(error CSV is required. Usage: make test MODEL=model.json CSV=file.csv)
endif
	cd $(PROJECT_ROOT)/model && python3 testmodel.py $(MODEL) $(CSV)

tune:
ifndef CSV
	$(error CSV is required. Usage: make tune CSV=file.csv)
endif
	cd $(PROJECT_ROOT)/model && python3 hyperparameter_tuning.py $(CSV)
