((nil . ((whitespace-action auto-cleanup)
	 (whitespace-style face empty trailing lines-tail)
	 (require-final-newline . t)
	 (mode . whitespace)))
 (org-mode . ((whitespace-style face empty trailing)
	      (eval .
		    (progn
                      (require 'org-version)
		      (setenv "PATH"
			      (concat "/home/ubuntu/InterpolationRepair/spot/bin"
				      path-separator
				      (getenv "PATH")))
                      (setenv "SPOT_UNINSTALLED" "1")
		      (setenv "PYTHONPATH"
			      (concat "/home/ubuntu/InterpolationRepair/spot/python/.libs:"
				      "/home/ubuntu/InterpolationRepair/spot/python:"
				      "/home/ubuntu/InterpolationRepair/spot/python:"
				      "/home/ubuntu/InterpolationRepair/spot/python/spot/.libs:"
				      "/home/ubuntu/InterpolationRepair/spot/python/spot:"
				      "/home/ubuntu/InterpolationRepair/spot/spot/ltsmin/.libs"
				      "/home/ubuntu/InterpolationRepair/spot/python/spot:"
				      (getenv "PYTHONPATH")))
		      (setenv "DYLD_LIBRARY_PATH"
			      (concat "/home/ubuntu/InterpolationRepair/spot/python/.libs:/home/ubuntu/InterpolationRepair/spot/spot/.libs:/home/ubuntu/InterpolationRepair/spot/buddy/src/.libs:"
				      (getenv "DYLD_LIBRARY_PATH")))
		      (setenv "SPOT_DOTDEFAULT" "Brf(Lato)C(#ffffa0)")
		      (setenv "SPOT_DOTEXTRA" "node[fontsize=12] fontsize=12 stylesheet=\"spot.css\" edge[arrowhead=vee, arrowsize=.7, fontsize=12]")
                      (setq org-babel-temporary-directory "/home/ubuntu/InterpolationRepair/spot/doc/org/tmp")
                      (make-directory org-babel-temporary-directory t)
		      (org-babel-do-load-languages 'org-babel-load-languages
                                                   `((,(if (version< org-version "8.3") 'sh 'shell) . t)
						     (python . t)
                                                     (plantuml . t)
						     (dot . t)
                                                     (R . t)
						     (C . t)))))
	      (org-confirm-babel-evaluate . nil)
              (org-plantuml-jar-path . "/home/ubuntu/InterpolationRepair/spot/doc/org/plantuml.jar")
	      (org-babel-python-command . "")
	      (org-babel-C++-compiler . "./g++wrap")
	      (shell-file-name . "/bin/bash")
              (ess-ask-for-ess-directory . nil)
              (org-export-html-postamble . nil)
              (org-html-table-header-tags
                 "<th scope=\"%s\"%s><div><span>" . "</span></div></th>")
              (org-babel-default-header-args:plantuml
               . ((:results . "file")
                  (:exports . "results")
                  ; Prevent the plantuml logo to annoying appear on
                  ; top of whatever you are doing when the project
                  ; compiles in the background.
                  (:java . "-Djava.awt.headless=true")))
	      (org-publish-project-alist
	       . (("spot-html"
		   :base-directory "."
		   :base-extension "org"
		   :publishing-directory "../userdoc/"
		   :recursive t
		   :exclude "setup.org"
		   :auto-sitemap t
		   :sitemap-title "Sitemap for Spot"
		   :publishing-function org-publish-org-to-html
		   :html-head "<link rel=\"stylesheet\" type=\"text/css\" href=\"spot.css\" />"
		   :auto-preamble t)
		  ("spot-static"
		   :base-directory "."
		   :base-extension "css\\|js\\|png\\|svg\\|jpg\\|gif\\|pdf"
		   :publishing-directory "../userdoc/"
		   :recursive t
		   :publishing-function org-publish-attachment)
		  ("spot-all" :components ("spot-html" "spot-static")))))))
