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

(let* ((seed0 10013)
       (seed  seed0))
  (defun reset-seed () (setf seed seed0))
  (defun park-miller-randomizer ()
    (let* ((multiplier 16807.0d0) ;16807 is (expt 7 5)
	   (modulus    2147483647.0d0)
	   (temp       (* multiplier seed)))
      (setf seed (mod temp modulus))
      (/ seed modulus)))
  (defun r (&optional (n 1.0))
    (let ((random-number (park-miller-randomizer)))
      (* n (- 1.0d0 random-number))))
  (defun rint (&optional (n 100))
    (let ((random-number (/ (r 1000.0) 1000)))
      (floor (* n random-number)))))

(defcol n num txt pos ignore (mean 0) (m2 0) min max (ns 0) sd)
(defcol s sym txt pos ignore (h (make-hash-table)) mode (most 0) )

(defmethod += ((s sym) x)
  (with-slots (h mode max) s
    (let* ((new (incf (gethash x h 0))))
      (if (> new max)
	  (setf max  new
		mode x))
      x)))

(defmethod += ((n num) x)
  (with-slots (mean m2 min max ns sd) n
    (incf ns)
    (let* ((delta (- x mean)))
      (setf mean (+ mean (/ delta ns))
	    m2   (+ (* delta (- x mean))))
      (if (> ns 2)
	  (setf sd (sqrt (/ m2 (- ns 1))))))
    x))

(defun* _n ()
  (let ((c (make-num)))
    (dotimes (i 10000)
      (+= c i))
    (print c)))

(defparameter *the*
  '((col . ((cache . ((max .  256)))))))

(defmacro z (&rest lst) `(ra ',lst *the*))
  
(defun ra (tags &optional (ra *the*))
  (let ((out ra))
    (dolist (tag tags out)
      (setf out (cdr (assoc tag out))))))

(let ((width (z col cache max)))
  (defstruct cache
    (ns    0)
    (all   (make-array width :initial-element 0))
    (max   width)
    (size  -1)))

(defmethod += ((c cache) x)
  (with-slots (ns all max size) c
    (incf ns)
    (if (< size (1- max))
	(setf (aref all (incf size)) x)
	(if (<= (r) (/ size ns))
	    (setf (aref all (floor (* (r) size))) x)))
    x))

(defun* _c ()
  (let ((c (make-cache)))
    (time (dotimes (i 10000)
      (+= c i)))
    (print (sort (cache-all c) #'<))))

(defmacro doitems ((one n list &optional out) &body body )
  `(let ((,n -1))
     (dolist (,one ,list ,out)  (incf ,n) ,@body)))

(defmacro docols ((cell head row tbl &optional out) &body body)
  `(mapcar
    #'(lambda (,cell ,head)
	(unless (slot-value ,header 'ignore)
	  ,@body))
    ,row
    (table-cols ,tbl)))

(defstruct table txt cols rows)

(defun data (&keys name cols rows)
  (labels ((ignorep (word) (find #\? (symbol-name word))))
    (let ((tbl (make-table)))
      (with-slots (cols row txt) tbl
	(setf txt  name
	      col  cols)
	  (dolist (row rows)
	  (docols (cell head row tbl)
		  (+= head cell))))
      tbl)))
	   
(defun weather ()
  (tbl
   :name   'weather
   :cols  (list (
   :rows    '((sunny 85 85 FALSE no)
	     (sunny 80 90 TRUE no)
	     (overcast 83 86 FALSE yes)
	     (rainy 70 96 FALSE yes)
	     (rainy 68 80 FALSE yes)
	     (rainy 65 70 TRUE no)
	     (overcast 64 65 TRUE yes)
	     (sunny 72 95 FALSE no)
	     (sunny 69 70 FALSE yes)
	     (rainy 75 80 FALSE yes)
	     (sunny 75 70 TRUE yes)
	     (overcast 72 90 TRUE yes)
	     (overcast 81 75 FALSE yes)
	     (rainy 71 91 TRUE no))))
