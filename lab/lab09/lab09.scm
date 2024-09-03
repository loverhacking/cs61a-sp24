(define (over-or-under num1 num2) 
  (if (>= num1 num2)
      (if (> num1 num2)
          1
          0)
      -1)
)
; if version

(define (over-or-under num1 num2) 
  (cond
    ((equal? num1 num2) 0)
    ((> num1 num2) 1)
    (else -1)))
; cond version

(define (make-adder num) 
  (lambda (inc) (+ num inc))) ;lambda versiom

(define (make-adder num) 
  (define (helper inc) 
    (+ inc num))
  helper) ;higher-order function versiom

(define (composed f g) 
  (lambda (x) (f (g x))))

(define (repeat f n) 
  (define (helper_repeat x)
  (if (= n 1) (f x)
    ((repeat f (- n 1)) (f x))))
  helper_repeat)

(define (max a b)
  (if (> a b)
      a
      b))

(define (min a b)
  (if (> a b)
      b
      a))

(define (gcd a b) 
  (if (zero? (modulo a b))
    (min a b)
    (gcd (min a b) (modulo (max a b) (min a b)))))

(define (skip-list lst filter-fn)
  (define (helper lst lst-so-far next)
    (cond
        ((null? lst)
            (if(null? next)
              lst-so-far
              (helper next lst-so-far nil))
        )
        ((list? (car lst))
          (helper (car lst) lst-so-far (append (cdr lst) next)))
        ((filter-fn (car lst))
          (helper (cdr lst) (append lst-so-far (list(car lst))) next))
        (else
          (helper (cdr lst) lst-so-far next))
    )
  )
  (helper lst nil nil)
)

;doctests
(expect (skip-list '(1 (3)) even?) ())
(expect (skip-list '(1 (2 (3 4) 5) 6 (7) 8 9) odd?) (1 3 5 7 9))
