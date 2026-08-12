# Équivalences MLX → Pygame

Ce document liste les fonctions Pygame utilisables dans un projet nécessitant
une librairie "similaire à la MLX", c'est-à-dire où chaque fonction utilisée
doit avoir un équivalent MLX direct.

## Tableau d'équivalences

| Fonction MLX | Équivalent Pygame | Explication |
|---|---|---|
| `mlx_init` | `pygame.init()` | Initialise la librairie |
| `mlx_release` | `pygame.quit()` | Libère les ressources / ferme la librairie |
| `mlx_new_window` | `pygame.display.set_mode((w, h))` + `pygame.display.set_caption(titre)` | Crée la fenêtre |
| `mlx_clear_window` | `screen.fill(couleur)` | Efface le contenu de la fenêtre |
| `mlx_pixel_put` | `screen.set_at((x, y), couleur)` | Affiche un pixel à une position |
| `mlx_destroy_window` | `pygame.display.quit()` | Détruit la fenêtre |
| `mlx_new_image` | `pygame.Surface((w, h))` | Crée une image/surface vide |
| `mlx_get_data_addr` | `pygame.surfarray.pixels3d(surface)` ou `surface.get_buffer()` | Accès direct aux données pixel d'une surface |
| `mlx_put_image_to_window` | `screen.blit(surface, (x, y))` | Affiche une image dans la fenêtre |
| `mlx_destroy_image` | *(pas d'équivalent explicite — GC automatique, `del surface` au plus proche)* | Détruit une image |
| `mlx_loop` | boucle `while running:` avec `pygame.event.get()` | Boucle principale d'événements |
| `mlx_loop_exit` | `pygame.event.post(pygame.event.Event(pygame.QUIT))` ou casser la boucle `while` | Quitte la boucle |
| `mlx_mouse_hook` | `pygame.MOUSEBUTTONDOWN` / `pygame.MOUSEMOTION` (via `pygame.event.get()`) | Callback souris |
| `mlx_key_hook` | `pygame.KEYDOWN` / `pygame.KEYUP` (via `pygame.event.get()`) | Callback clavier |
| `mlx_expose_hook` | `pygame.VIDEOEXPOSE` | Callback de rafraîchissement |
| `mlx_loop_hook` | appel de fonction à chaque itération de la boucle `while` | Callback à chaque tour de boucle |
| `mlx_hook` | `pygame.event.get()` (gestion générique d'un type d'event) | Callback générique |
| `mlx_string_put` | `font.render(texte, ...)` + `screen.blit(...)` (via `pygame.font`) | Affiche du texte |
| `mlx_xpm_file_to_image` | `pygame.image.load("fichier.xpm")` | Charge une image XPM |
| `mlx_png_file_to_image` | `pygame.image.load("fichier.png")` | Charge une image PNG |
| `mlx_mouse_hide` | `pygame.mouse.set_visible(False)` | Cache le curseur |
| `mlx_mouse_show` | `pygame.mouse.set_visible(True)` | Affiche le curseur |
| `mlx_mouse_move` | `pygame.mouse.set_pos((x, y))` | Déplace le curseur |
| `mlx_mouse_get_pos` | `pygame.mouse.get_pos()` | Récupère la position du curseur |
| `mlx_do_key_autorepeatoff` | `pygame.key.set_repeat(0)` | Désactive la répétition de touches |
| `mlx_do_key_autorepeaton` | `pygame.key.set_repeat(delay, interval)` | Active la répétition de touches |
| `mlx_get_screen_size` | `pygame.display.Info()` (`.current_w`, `.current_h`) | Taille de l'écran |
| `mlx_do_sync` | `pygame.display.flip()` ou `pygame.display.update()` | Synchronise/rafraîchit l'affichage |
| `mlx_sync` | `pygame.display.update(rect)` (sur une zone spécifique) | Synchronise une zone |

## Fonctions Pygame à éviter

Ces fonctions n'ont **aucun équivalent MLX** dans la liste fournie et sont donc
à considérer comme interdites selon la règle "chaque fonction doit avoir un
équivalent MLX" :

- `pygame.draw.*` (cercles, rectangles, lignes tout faits) — MLX n'a que `pixel_put`, pas de primitives de dessin haut niveau
- `pygame.transform.*` (rotate, scale, flip)
- `pygame.mixer.*` (son/musique)
- `pygame.sprite.*` (groupes de sprites, collisions automatiques)
- `pygame.time.Clock()` — pas d'équivalent direct listé (voir note ci-dessous)

## Note sur la gestion du temps (FPS)

Si le projet nécessite un FPS cap ou une gestion du temps, il faut vérifier
avec l'énoncé exact si `mlx_loop_hook` (appelé à chaque tick) est censé couvrir
ce rôle. Dans la vraie MLX, c'est souvent via `mlx_loop_hook` qu'on gère le
timing, donc `pygame.time.Clock().tick(fps)` pourrait être accepté comme
équivalent fonctionnel raisonnable — à valider selon les consignes précises
du sujet.