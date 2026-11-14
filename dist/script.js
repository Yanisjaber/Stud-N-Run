const menuButton = document.querySelector('.menu-toggle');
const navigation = document.getElementById('navigation-principale');
const mobileLayout = window.matchMedia('(max-width: 760px)');

function setMenuOpen(open) {
  navigation.hidden = !open;
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.textContent = open ? 'Fermer le menu' : 'Menu';
}

function adaptNavigation() {
  const focusWasInNavigation = navigation.contains(document.activeElement);
  const focusWasOnButton = document.activeElement === menuButton;

  menuButton.hidden = !mobileLayout.matches;
  setMenuOpen(!mobileLayout.matches);

  if (mobileLayout.matches && focusWasInNavigation) {
    menuButton.focus();
  } else if (!mobileLayout.matches && focusWasOnButton) {
    navigation.querySelector('[aria-current="page"]').focus();
  }
}

menuButton.addEventListener('click', () => setMenuOpen(navigation.hidden));
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && mobileLayout.matches && !navigation.hidden) {
    setMenuOpen(false);
    menuButton.focus();
  }
});
mobileLayout.addEventListener('change', adaptNavigation);
adaptNavigation();
