package aitl

#OutcomeRequest: {
	kind:         _
	areas_listed: _
	if kind == "development" {
		// ADR-005@v3 C1: work built into the exemplar by hand comes from a development outcome (DEV-1 to DEV-3)
		id: =~"^DEV-[1-3]$"
	}
	// ADR-005@v3 C6: a development outcome changes only the areas listed for it
	areas_touched: [...or(areas_listed)]
}
