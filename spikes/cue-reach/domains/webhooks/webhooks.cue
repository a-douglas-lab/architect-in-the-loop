package webhooks

import (
	"aitl.example/domains/canon"
	"aitl.example/domains/policy/data"
)

// Webhooks ADR C1: webhooks forward the tracking number as text
#ShippedHook: canon.#OrderShipped & {trackingNumber: string}

// Webhooks ADR C2: the carriers webhooks support
supportedCarriers: [...canon.#Carrier] & ["royal-mail", "ups", "DHL"]

sample: #ShippedHook & {orderId: "o-1", carrier: "DHL", trackingNumber: "TRK123"}

events: delivered: data.#Event & {
	name:          "HookDelivered"
	schemaVersion: 1
	retentionDays: 180
	payload:       sample
}
