(define (problem smart-building-situation)
  (:domain smart-office)

  (:init
    (meeting-scheduled)
    (high-co2)
  )

  (:goal
    (and (ventilated) (alert-sent) (email-sent))
  )
)