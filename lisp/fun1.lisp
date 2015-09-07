

(defparameter *tries* 0)
(defparameter *fails* 0)

(defmacro strive (&body code)
  (let ((pass   (gensym))
	(err    (gensym)))
    `(multiple-value-bind (,pass ,err)
	 (ignore-errors
	   (incf *tries*)
	     ,@code)
       (if ,pass
	   (print `(pas ,pass))
	   (progn
	     (incf *fails*)
	     (format t "~&~s% :: ~A~%"
		     (round (* 100 (/ *tries*
				      (+ *tries* *fails*))))
		     ,err))))))

(defmacro defun* (name parameters &body body)
  `(progn 
     (defun ,name ,parameters ,@body)
     (format t "~%;;; ~s~%" ',name)
     (strive (,name))))



(defun bb ()
  (assert (> 11 10)))

(defun* aa()
  (bb))


