(define (curry-cook formals body) 
  (if (null? formals)
    body
    (list 'lambda (list (car formals)) (curry-cook (cdr formals) body)))
)
;doctests
(expect (curry-cook '(a) 'a) (lambda (a) a))
(expect (curry-cook '(x y) '(+ x y)) (lambda (x) (lambda (y) (+ x y))))


(define (curry-consume curry args)
  (if (null? args)
    curry
    (curry-consume (curry (car args)) (cdr args))
  ) 
)
;doctests
(expect (curry-consume (lambda (x) (lambda (y) (lambda (z) (+ x (* y z))))) '(1 2 3)) 7)


(define-macro (switch expr options)
  (switch-to-cond (list 'switch expr options)))

(define (switch-to-cond switch-expr)
  (cons 'cond
        (map (lambda (option)
               (cons (list 'equal? (car (cdr switch-expr)) (car option)) (cdr option)))
             (car (cdr (cdr switch-expr))))))
;doctests
(expect (switch-to-cond `(switch (+ 1 1) ((1 2) (2 4) (3 6))))
  (cond ((equal? (+ 1 1) 1) 2) ((equal? (+ 1 1) 2) 4) ((equal? (+ 1 1) 3) 6)))


;from Fall 2019 Final Q9: Macro Lens
;; A macro that creates a procedure from a partial call expression missing the last operand.
;; (define add-two (partial (+ 1 1))) -> (lambda (y) (+ 1 1 y))
;; (add-two 3) -> 5 by evaluating (+ 1 1 3)
;;
;; (define eq-5 (partial (equal? (+ 2 3)))) -> (lambda (y) (equal? (+ 2 3) y))
;; (eq-5 (+ 3 2)) -> #t by evaluating (equal? (+ 2 3) 5)
;;
;; ((partial (append '(1 2))) '(3 4)) -> (1 2 3 4)
(define-macro (partial call)
`(lambda (y), (append call (list 'y)))
)

;doctests
(expect ((partial (+ 1 1)) 3) 5)
(expect ((partial (equal? (+ 2 3))) (+ 3 2)) #t)
(expect ((partial (append '(1 2))) '(3 4)) (1 2 3 4))


;from Summer 2019 Final Q7c: Slice

(define-macro (slice f at k)
  `(lambda (x) (, f (+ x, k)))
)

(define (h x)
  (+ x 2))

;doctests
(expect ((slice h at 3) 2) 7)


;from Spring 2019 Final Q8: Macros
(define-macro (if condition then else
  '(or (and condition then) (and condition else))
  )
)
(expect (if #t 1 (/ 1 0)) 1)
(expect (if #f 1 (+ 1 1)) 2)