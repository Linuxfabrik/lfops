TODO

Creating an Admin and a user:

nextcloud__users:
  - username: 'thefirstadmin'
    password: 'gkKZG5ojbdJYh86wquGMzNDe6OnDA8tHzA3NRepT'
    group: 'admin'
    settings:
      - 'core lang en'
      - 'core locale de_CH'
      - 'core timezone Europe/Zurich'
      - 'files quota "50 MB"'
      - 'firstrunwizard show 0'
      - 'settings email info@example.org'
  - username: 'john.doe'
    password: 'w7MVoIfuaewX8Gs9Ds8vFqcYx1P9Vtd95fJpHIJt'
