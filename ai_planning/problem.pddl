(define (problem smart-building-situation)
  (:domain smart-office)

  (:init
    (meeting-scheduled)
  )

  (:goal
    (and (send-meeting-scheduled))
  )
)