

(function(globals) {

  var django = globals.django || (globals.django = {});


  django.pluralidx = function(n) {
    var v=(n > 1);
    if (typeof(v) == 'boolean') {
      return v ? 1 : 0;
    } else {
      return v;
    }
  };


  /* gettext library */

  django.catalog = django.catalog || {};

  var newcatalog = {
    "%(sel)s of %(cnt)s selected": [
      "%(sel)s sur %(cnt)s s\u00e9lectionn\u00e9",
      "%(sel)s sur %(cnt)s s\u00e9lectionn\u00e9s"
    ],
    "(filtered from _MAX_ total entries)": "(filtr\u00e9 de _MAX_ \u00e9l\u00e9ments au total)",
    "6 a.m.": "6:00",
    "6 p.m.": "18:00",
    ": activate to sort column ascending": ": activer pour trier la colonne par ordre croissant",
    "April": "Avril",
    "August": "Ao\u00fbt",
    "Available %s": "%s disponible(s)",
    "Cancel": "Annuler",
    "Choose": "Choisir",
    "Choose a Date": "Choisir une date",
    "Choose a Time": "Choisir une heure",
    "Choose a time": "Choisir une heure",
    "Choose all": "Tout choisir",
    "Chosen %s": "Choix des \u00ab\u00a0%s \u00bb",
    "Click to choose all %s at once.": "Cliquez pour choisir tous les \u00ab\u00a0%s\u00a0\u00bb en une seule op\u00e9ration.",
    "Click to remove all chosen %s at once.": "Cliquez pour enlever tous les \u00ab\u00a0%s\u00a0\u00bb en une seule op\u00e9ration.",
    "Close all": "Fermer tout",
    "Collapse": "Fermer",
    "Copy": "Copier",
    "Cut": "Couper",
    "December": "D\u00e9cembre",
    "Detach": "D\u00e9tacher",
    "Error(s) in form: The modifications are not saved": "Erreur(s) dans le formulaire: Les modifications n'ont pas \u00e9t\u00e9 enregistr\u00e9es",
    "Existed code for ": "Code a d\u00e9j\u00e0 exist\u00e9 pour ",
    "Existed name version in ": "Cette version existe dans le pass\u00e9 en ",
    "Existing code in ": "Code d\u00e9j\u00e0 existant en ",
    "Existing name version": "Cette version existe d\u00e9j\u00e0",
    "February": "F\u00e9vrier",
    "Filter": "Filtrer",
    "First": "Premier",
    "Forbidden because of prerequisites": "Interdit \u00e0 cause des pr\u00e9requis",
    "Hide": "Masquer",
    "Insertion of a link to a CDN document": "Insertion d'un lien vers un document du CDN",
    "Invalid code": "Code non valide",
    "Invalid name version": "Sigle de version invalide",
    "January": "Janvier",
    "July": "Juillet",
    "June": "Juin",
    "Last": "Dernier",
    "Link to CDN Doc": "Lien vers document du CDN",
    "Loading...": "Chargement en cours...",
    "March": "Mars",
    "May": "Mai",
    "Midnight": "Minuit",
    "Modify the link": "Modifier le lien",
    "New version": "Nouvelle version",
    "Next": "Suivant",
    "No data available in table": "Aucune donn\u00e9e disponible dans le tableau",
    "No matching records found": "Aucun \u00e9l\u00e9ment \u00e0 afficher",
    "Noon": "Midi",
    "Note: You are %s hour ahead of server time.": [
      "Note\u00a0: l'heure du serveur pr\u00e9c\u00e8de votre heure de %s heure.",
      "Note\u00a0: l'heure du serveur pr\u00e9c\u00e8de votre heure de %s heures."
    ],
    "Note: You are %s hour behind server time.": [
      "Note\u00a0: votre heure pr\u00e9c\u00e8de l'heure du serveur de %s heure.",
      "Note\u00a0: votre heure pr\u00e9c\u00e8de l'heure du serveur de %s heures."
    ],
    "November": "Novembre",
    "Now": "Maintenant",
    "October": "Octobre",
    "Open": "Ouvrir",
    "Open all": "Ouvrir tout",
    "Paste": "Coller",
    "Please enter a valid URL.": "Entrez une URL valide.",
    "Please enter a value greater than or equal to 0.": "Veuillez entrer une valeur sup\u00e9rieure ou \u00e9gale \u00e0 0.",
    "Please enter a value less than or equal to 500.": "Veuillez entrer une valeur inf\u00e9rieure ou \u00e9gale \u00e0 500.",
    "Please enter a value that is a multiple of 0.5.": "Veuillez entrer une valeur qui est un multiple de 0,5.",
    "Please use the Ctrl+v shortcut to paste content.": "Vous devez utiliser le raccourci Ctrl+V pour coller.",
    "Previous": "Pr\u00e9c\u00e9dent",
    "Processing...": "Traitement en cours...",
    "Prolong": "Prolonger",
    "Remove": "Enlever",
    "Remove all": "Tout enlever",
    "Search": "Rechercher",
    "Search by name:": "Rechercher par nom:",
    "Selection of target files": "S\u00e9lection du fichier cible",
    "September": "Septembre",
    "Show": "Afficher",
    "Show _MENU_ entries": "Afficher _MENU_ \u00e9l\u00e9ments",
    "Showing 0 to 0 of 0 entries": "Affichage de l'\u00e9l\u00e9ment 0 \u00e0 0 sur 0 \u00e9l\u00e9ment",
    "Showing _START_ to _END_ of _TOTAL_ entries": "Affichage de l'\u00e9l\u00e9ment _START_ \u00e0 _END_ sur _TOTAL_ \u00e9l\u00e9ments",
    "The learning unit %(code)s will be published soon.": "L'unit\u00e9 d'enseignement %(code)s sera publi\u00e9 sous peu.",
    "This field is required": "Ce champ est obligatoire.",
    "This is the list of available %s. You may choose some by selecting them in the box below and then clicking the \"Choose\" arrow between the two boxes.": "Ceci est une liste des \u00ab\u00a0%s\u00a0\u00bb disponibles. Vous pouvez en choisir en les s\u00e9lectionnant dans la zone ci-dessous, puis en cliquant sur la fl\u00e8che \u00ab\u00a0Choisir\u00a0\u00bb entre les deux zones.",
    "This is the list of chosen %s. You may remove some by selecting them in the box below and then clicking the \"Remove\" arrow between the two boxes.": "Ceci est la liste des \u00ab\u00a0%s\u00a0\u00bb choisi(e)s. Vous pouvez en enlever en les s\u00e9lectionnant dans la zone ci-dessous, puis en cliquant sur la fl\u00e8che \u00ab Enlever \u00bb entre les deux zones.",
    "Today": "Aujourd'hui",
    "Tomorrow": "Demain",
    "Type into this box to filter down the list of available %s.": "\u00c9crivez dans cette zone pour filtrer la liste des \u00ab\u00a0%s\u00a0\u00bb disponibles.",
    "Yesterday": "Hier",
    "You can't extend the transition version '{full_code}' in {year} as other transition version exists in {transition_year}": "Vous ne pouvez pas \u00e9tendre la version de transition '{full_code}' en {year} parce qu'il existe une autre version de transition en {transition_year}",
    "You have selected an action, and you haven't made any changes on individual fields. You're probably looking for the Go button rather than the Save button.": "Vous avez s\u00e9lectionn\u00e9 une action, et vous n'avez fait aucune modification sur des champs. Vous cherchez probablement le bouton Envoyer et non le bouton Enregistrer.",
    "You have selected an action, but you haven't saved your changes to individual fields yet. Please click OK to save. You'll need to re-run the action.": "Vous avez s\u00e9lectionn\u00e9 une action, mais vous n'avez pas encore sauvegard\u00e9 certains champs modifi\u00e9s. Cliquez sur OK pour sauver. Vous devrez r\u00e9appliquer l'action.",
    "You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost.": "Vous avez des modifications non sauvegard\u00e9es sur certains champs \u00e9ditables. Si vous lancez une action, ces modifications vont \u00eatre perdues.",
    "You should make a selection before clicking 'ok'": "Vous devez faire une s\u00e9l\u00e9ction avant de cliquer sur 'ok'",
    "activate to sort column ascending": "activer pour trier la colonne par ordre croissant",
    "activate to sort column descending": "activer pour trier la colonne par ordre d\u00e9croissant",
    "one letter Friday\u0004F": "V",
    "one letter Monday\u0004M": "L",
    "one letter Saturday\u0004S": "S",
    "one letter Sunday\u0004S": "D",
    "one letter Thursday\u0004T": "J",
    "one letter Tuesday\u0004T": "M",
    "one letter Wednesday\u0004W": "M"
  };
  for (var key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }


  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      var value = django.catalog[msgid];
      if (typeof(value) == 'undefined') {
        return msgid;
      } else {
        return (typeof(value) == 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      var value = django.catalog[singular];
      if (typeof(value) == 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      var value = django.gettext(context + '\x04' + msgid);
      if (value.indexOf('\x04') != -1) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      var value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.indexOf('\x04') != -1) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "j F Y H:i",
    "DATETIME_INPUT_FORMATS": [
      "%d/%m/%Y %H:%M:%S",
      "%d/%m/%Y %H:%M:%S.%f",
      "%d/%m/%Y %H:%M",
      "%d/%m/%Y",
      "%d.%m.%Y %H:%M:%S",
      "%d.%m.%Y %H:%M:%S.%f",
      "%d.%m.%Y %H:%M",
      "%d.%m.%Y",
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%Y-%m-%d"
    ],
    "DATE_FORMAT": "j F Y",
    "DATE_INPUT_FORMATS": [
      "%d/%m/%Y",
      "%d/%m/%y",
      "%d.%m.%Y",
      "%d.%m.%y",
      "%Y-%m-%d"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 1,
    "MONTH_DAY_FORMAT": "j F",
    "NUMBER_GROUPING": 3,
    "SHORT_DATETIME_FORMAT": "j N Y H:i",
    "SHORT_DATE_FORMAT": "j N Y",
    "THOUSAND_SEPARATOR": "\u00a0",
    "TIME_FORMAT": "H:i",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F Y"
  };

    django.get_format = function(format_type) {
      var value = django.formats[format_type];
      if (typeof(value) == 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }

}(this));

