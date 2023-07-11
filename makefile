NAME = version-counter

build:
	@ cd src \
		&& { find . -type d ! -name "__pycache__" & find . -type f -name "*.py"; } \
		| zip ../$(NAME).zip -@

	@ echo '#!/usr/bin/env python3' | cat - $(NAME).zip > $(NAME)
	@ rm -f $(NAME).zip
