package ordering

import (
	"aitl.example/domains/canon"
	"aitl.example/domains/policy/auth"
	"aitl.example/domains/policy/data"
	"aitl.example/domains/capability/workflow"
)

// Ordering ADR C1: an order's status is one of these
#OrderStatus: "submitted" | "paid" | "shipped" | "cancelled"

#Order: {
	id:     string
	status: #OrderStatus
}

sampleOrder: #Order & {id: "o-1", status: "shipped"}

endpoints: [...auth.#Endpoint] & [
	{path: "/orders", method: "POST", auth: "required", roles: ["customer"], admin: false, mfa: false},
	{path: "/orders/admin/cancel", method: "POST", auth: "required", roles: ["ops"], admin: true, mfa: false},
]

events: shipped: data.#Event & {
	name:          "OrderShipped"
	schemaVersion: 1
	retentionDays: 90
	payload: canon.#OrderShipped & {orderId: "o-1", carrier: "DHL", trackingNumber: "TRK123"}
}

workflows: fulfil: workflow.#Workflow & {
	name: "fulfil-order"
	steps: [{name: "reserve-stock", sideEffect: true, timeoutHours: 2, compensation: "release-stock"}]
}
