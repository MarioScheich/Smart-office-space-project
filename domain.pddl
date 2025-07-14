(define (domain smart-office)

  (:requirements :strips :typing)

  (:types room)

  (:predicates
    (occupied)
    (meeting-scheduled)
    (high-co2)
    (high-humidity)
    (too-cold)
    (window-opened)
    (alert-sent)
    (ventilated)
    (light-on)
    (buzzer-on)
  )

  (:action open-window
    :precondition (and occupied (not high-co2) (not high-humidity) (not too-cold))
    :effect (and (window-opened) (ventilated))
  )

  (:action close-window
    :precondition (window-opened)
    :effect (not window-opened)
  )

  (:action turn-on-light
    :precondition (or meeting-scheduled occupied)
    :effect (light-on)
  )

  (:action turn-off-light
    :precondition (not occupied)
    :effect (not light-on)
  )

  (:action send-alert
    :precondition (high-co2)
    :effect (alert-sent)
  )

  (:action activate-buzzer
    :precondition (and meeting-scheduled occupied)
    :effect (buzzer-on)
  )
)
 