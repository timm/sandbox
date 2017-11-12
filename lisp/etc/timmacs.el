;;;; pacakge stuff

(progn 
  (defvar my-packages '(slime helm powerline 
                              better-defaults paredit
                              idle-highlight-mode
                              ido-ubiquitous
                              find-file-in-project magit smex scpaste))
  (package-initialize)
  (dolist (p my-packages)
    (when (not (package-installed-p p))
      (package-install p))))

;;;; a few of my favorite things
(progn
  (setq ispell-program-name "/usr/local/bin/ispell")
  (setq tab-width 2)
  (setq inhibit-startup-message t)
  (setq make-backup-files nil)
  (xterm-mouse-mode t)
  (menu-bar-mode 1)
  (setq scroll-step 1)
  (global-linum-mode 1)
  (require 'ido)
  (ido-mode t)
  (global-hl-line-mode)
  (recentf-mode 1)
  (setq ess-fancy-comments nil)
  (setq recentf-max-menu-items 25)
  (global-set-key "\C-x\ \C-r" 'recentf-open-files)
  (global-set-key (kbd "C-x g") 'magit-status) 
  (setq-default frame-title-format
              '(:eval
                (format "%s %s"
                        
                        (buffer-name)
                        (cond
                         (buffer-file-truename
                          (concat "(" buffer-file-truename ")"))
                         (dired-directory
                          (concat "{" dired-directory "}"))
                         (t
                          "[no file]")))))
)
;;;; general lisp things


(progn
  (require 'slime)
  (require 'slime-autoloads)
  (setq inferior-lisp-program "/usr/local/bin/sbcl")
  (add-to-list 'load-path "/usr/local/bin/sbcl")


  (add-hook 'slime-mode-hook '(lambda () 
                              (unless (get-process "SLIME Lisp")
                                (slime))))

  
  (add-hook 'inferior-lisp-mode-hook (lambda () (inferior-slime-mode t)))
  (setq inferior-lisp-program "/usr/local/bin/sbcl"
       slime-contribs '(slime-fancy))
  )


;;;; my specific list things

(progn
  (font-lock-add-keywords
   'lisp-mode
   '(("deftest" . font-lock-keyword-face)
     ("dohash" . font-lock-keyword-face)
     ("defklass" . font-lock-keyword-face)
     ("defthing" . font-lock-keyword-face)
     ("deftable" . font-lock-keyword-face)
     ("doitems" . font-lock-keyword-face)))
  
  (put 'deftest 'lisp-indent-function 'defun)
  (put 'defklass  'lisp-indent-function 'defun)
  (put 'defthing 'lisp-indent-function 'defun)
  (put 'deftable 'lisp-indent-function 'defun)
  (put 'dohash 'lisp-indent-function 'defun)
  (put 'doitems 'lisp-indent-function 'defun)
  )



