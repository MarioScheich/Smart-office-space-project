(define (domain smart-office)

  (:requirements :strips :typing)

  (:types room person)

  (:predicates
    (occupied)
    (meeting-scheduled)
    (high-co2)
    (high-humidity)
    (too-cold)
    (rain-expected)
    (forecast-bad)
    (window-opened)
    (alert-sent)
    (ventilated)
    (light-on)
    (buzzer-on)
    (email-sent)
  )

  ;; ✅ Open window if (high-co2 OR high-humidity) AND not (too-cold)
  (:action open-window
    :precondition (and (or (high-co2) (high-humidity)) (not (too-cold)))
    :effect (and (window-opened) (ventilated))
  )

  ;; ✅ Close window if cold or rain expected
  (:action close-window
    :precondition (or (rain-expected) (too-cold))
    :effect (not (window-opened))
  )

  ;; ✅ Turn on light if occupied
  (:action turn-on-light
    :precondition (occupied)
    :effect (light-on)
  )

  ;; ✅ Turn off light if NOT occupied
  (:action turn-off-light
    :precondition (not (occupied))
    :effect (not (light-on))
  )

  ;; ✅ Activate buzzer if high CO2
  (:action activate-buzzer
    :precondition (high-co2)
    :effect (buzzer-on)
  )

  ;; ✅ Send email update if forecast changed and meeting scheduled
  (:action send-email-weather-update
    :precondition (and (forecast-bad) (meeting-scheduled))
    :effect (email-sent)
  )
)