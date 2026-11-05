package samepkg

// ...and the consumer declares its rule on the same definition in the same package, instead of
// importing and refining it. Consumer ADR C1: the tracking number is forwarded as text.
#OrderShipped: {trackingNumber: string}

example: #OrderShipped & {orderId: "o-1", trackingNumber: "T1"}
