package workflow

// A shared capability used by several domains, with its own ADR.

maxStepTimeoutHours: 24

#Step: {
	name:         string
	sideEffect:   bool
	timeoutHours: int & >0 & <=maxStepTimeoutHours
	compensation?: string
	if sideEffect {
		// Workflow ADR C1: a step with a side effect has a compensation
		compensation: string
	}
}

#Workflow: {
	name: string
	steps: [_, ...] & [...#Step]
}
