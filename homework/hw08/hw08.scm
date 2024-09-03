(define (ascending? s) 
    (if (or (null? s) (null? (cdr s)))
        #t
        (if (> (car s) (car (cdr s)))
            #f
            (ascending? (cdr s))
        )
    )
)

(define (my-filter pred s) 
    (if (null? s)
        s
        (if (pred (car s))
            (cons (car s) (my-filter pred (cdr s)))
            (my-filter pred (cdr s))
        )
    )
)

(define (interleave lst1 lst2) 
    (if (or (null? lst1) (null? lst2))
        (append lst1 lst2)
        (cons (car lst1) 
            (cons(car lst2)
                (interleave (cdr lst1) (cdr lst2))))
    )
)

; Alternate Solution
(define (interleave lst1 lst2)
  (cond 
    ((null? lst1)
     lst2)
    ((null? lst2)
     lst1)
    (else
     (cons (car lst1) (interleave lst2 (cdr lst1))))))

(define (no-repeats s) 
    (if (null? s)
        s
        (if (null? (filter (lambda (x) (= (car s) x)) (cdr s)))
            (cons (car s) (no-repeats (cdr s)))
            (no-repeats (cdr s))
        )
    )
)


;from Fall 2022 Final, Question 8: A Parentheses Scheme
(define (remove-parens s)
    (cond
    ( (null? s) nil )
    ( (list? (car s)) (append (remove-parens (car s)) (remove-parens (cdr s))))
    ( else (cons (car s) (remove-parens (cdr s))))))
; Doctests
(expect (remove-parens '(((1) 2 3) 4 5 (6 (7)) (8 10))) (1 2 3 4 5 6 7 8 10))
(expect (remove-parens '(((a) b (c) ()) (d) e (f (((g)))) (h i))) (a b c d e f g h i))


;from Spring 2022 Final, Question 11: Beadazzled, The Scheme-quel
(define (make-necklace beads length)
; Returns a list where each value is taken from the BEADS list,
; repeating the values BEADS until the list has reached
; LENGTH. You can assume that LENGTH is greater than or equal to 1,
; and that there is at least one bead in BEADS.
    (if (= length 0)
        ; (a)
        nil
        ; (b)
        (cons (car beads)
             ;(c)
            (make-necklace
            (append (cdr beads) (cons (car beads) nil))
            ; (d)
            (- length 1)
            ; (e)
            )
        )
    )
)
; Doctests
(expect (make-necklace '(~ *) 3) (~ * ~))
(expect (make-necklace '(~ ^) 4) (~ ^ ~ ^))
(expect (make-necklace '(> 0 <) 9) (> 0 < > 0 < > 0 <))


; from Fall 2021 Final, Question 4: Spice
;(a)
;;; Construct a repeated call expression from an operator and a list of operands.

(define (repeated-call operator operands)
    (if (null? operands)
    operator
    (repeated-call (cons operator (cons (car operands) nil)) (cdr operands))))
    ;(a)                           (b)                             (c)
; Doctests
(expect (repeated-call 'f '(2 3 4)) (((f 2) 3) 4))
(expect (repeated-call '(f 2) '(3 4)) (((f 2) 3) 4))
(expect (repeated-call 'f nil) f)

;(b)
;;; Return a curried version of f that can be called repeatedly num-args times.
(define (curry num-args)
    (lambda (f) (curry-helper num-args (lambda (s) (apply f s)))))

;;; curry-helper's argument g is a one-argument procedure that takes a list.
(define (curry-helper num-args g)
    (if (= num-args 0)
        (g nil)
        ;(a)
    (lambda (x) (curry-helper (- num-args 1) (lambda (s) (g (cons x s)))))))
                                                    ;(b)
; Doctests
(expect (((((curry 3) +) 4) 5) 6) 15)
(expect ((curry 0) +) 0)
(expect (((curry 1) +) 3) 3) 
(expect (((((curry 3) list) 4) 5) 6) (4 5 6))
(expect ((((curry-helper 3 cdr) 5) 6) 7) (6 7))

;(c)
;;; Take a (possibly nested) call expression s and return
;;; an equivalent expression in which all calls have one argument.

(define (one-arg s)
    (if (number? s) s
        (let ((num-args (- (length s) 1)))
            (if (= num-args 1)
                (list (car s) (one-arg (car (cdr s))))
                ;(a)    (b)                  (c)
                (repeated-call (list (list 'curry num-args) (car s))
                                          ;(d)                 (e)
                    (map one-arg (cdr s)))))))
                           ;(f)
; Doctests
(expect (one-arg '(abs 3)) (abs 3))
(expect (one-arg '(+ 4 5 6)) (((((curry 3) +) 4) 5) 6))
(expect (eval (one-arg '(+ 4 5 6))) 15)
(expect (one-arg '(+ (- 4) (*) (* 5 6))) (((((curry 3) +) (- 4)) ((curry 0) *)) ((((curry 2) *) 5) 6)))