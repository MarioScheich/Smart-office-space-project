(define (problem smart-building-situation)
  (:domain smart-office)

  (:init
    (high-co2)
  )

  (:goal
    (and (ventilated) (alert-sent) (email-sent))
  )
)