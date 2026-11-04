package aitl

// The shared definitions. Each adrNNN.cue file in this package adds its clauses to them, and
// CUE unifies every file of a package, so loading the package loads every ADR's clauses at once.

#OutcomeRequest: {
	id:            string
	outcome:       string
	stated_by:     string
	kind:          "development" | "evaluation"
	areas_listed:  [...string]
	areas_touched: [...string]
	examples: {
		visible: [...string]
		hidden:  [...string]
	}
	applies: [string]: bool
}

#PlanCitations: {
	adrs:      [...string]
	citations: [...string]
}

// The data file supplies these two.
request: #OutcomeRequest
plan:    #PlanCitations
