;; (DEFINE (member_list atm a_list)
;;     (COND
;;         ((NULL? a_list) #F)
;;         ((EQ? atm (CAR a_list)) #T)
;;         (ELSE (member_list atm (CDR a_list)))
;;     )
;; )

;; (member_list 9 '(1 2 3 4 5))

(DEFINE (equalsimp list1 list2)
    (COND
        ((NULL? list1) (NULL? list2))
        ((NULL? list2) #F)
        ((EQ? (CAR list1) (CAR list2)) (equalsimp (CDR list1) (CDR list2)))
    )
)

(equalsimp '(A B C) '(A B C D))
