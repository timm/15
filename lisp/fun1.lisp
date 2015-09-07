(defparameter *all* 0)
(defparameter *bad* 0)

(defmacro strive (name &body code)
  (let ((err (gensym)))
    `(progn
       (handler-case
	   (progn
	     (format t ";;; ~s" ,name)
	     (incf *all*)
	     ,@code)
	 (error (,err)
	   (incf *bad*)
	   (format t " ~3D%: ~A"
		   (round (* 100.0 (/ *all*
			     (+ *all* *bad*))))
		   ,err)))
       (format t "~&"))))

(defmacro defun* (name parameters &body body)
  `(progn 
     (defun ,name ,parameters ,@body)
     (strive ',name (,name))))

(defun whiteout (seq)
  (remove-if (lambda (char)
	       (member char '(#\Space #\Tab
			      #\Newline #\Page)
		       :test #'char=))
	     seq))

(defun samep (thing1 thing2)
  (string= (string-downcase (whiteout (format nil "~a" thing1)))
	   (string-downcase (whiteout (format nil "~a" thing2)))))

(defun cc (n)
  (assert (> 11 n))
  )

(defun bb (n)
  (cc n))

(defun* aa (&optional (n 1))
  n
  )

(defun* ll ()
  (bb 100))

(defun* mm()
  t)

(defun maker (klass val &optional (slot 'txt))
  (let ((tmp (make-instance klass)))
    (setf (slot-value tmp slot) val)
    tmp))

(defmacro defcol (sym klass &rest slots)
  `(progn
     (defstruct ,klass ,@slots)
     (defun ,sym (x) (maker  ',klass x))))

 ;[ ] { } ! ?

(defcol n num (sum 0) (sumsq 0) min max ns)
(defcol s sym (h (make-hash-table)) mode max)

(defmethod += ((s sym) x)
  (with-slots (h mode max) s
    (unless mode (setf mode x))
    (unless max  (setf mode x))
    (setf (gethash x h)
;(print (list ^forecast $temp $humidty ^wind !play))

;; (defun make-some-weather-data ()
;;   (data
;;    :name   'weather
;;    :columns  12
;;    :egs    '((sunny 85 85 FALSE no)
;; 	     (sunny 80 90 TRUE no)
;; 	     (overcast 83 86 FALSE yes)
;; 	     (rainy 70 96 FALSE yes)
;; 	     (rainy 68 80 FALSE yes)
;; 	     (rainy 65 70 TRUE no)
;; 	     (overcast 64 65 TRUE yes)
;; 	     (sunny 72 95 FALSE no)
;; 	     (sunny 69 70 FALSE yes)
;; 	     (rainy 75 80 FALSE yes)
;; 	     (sunny 75 70 TRUE yes)
;; 	     (overcast 72 90 TRUE yes)
;; 	     (overcast 81 75 FALSE yes)
;; 	     (rainy 71 91 TRUE no))))
