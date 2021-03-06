from syfertext.doc import Doc
from syfertext.token import Token
from typing import Union


class SimpleTagger:
    """This is a very simple token-level tagger. It enables to tag specified
       tokens in a `Doc` object. By tagging a token, we mean setting a new
       attribute to that token which holds the desired tag as its value.
       The attribute becomes accessible then through the Underscore attribute
       of the `Token` object.
    """

    def __init__(
        self,
        attribute: str,
        lookups: Union[set, list, dict],
        tag: object = None,
        default_tag: object = None,
        case_sensitive: bool = True,
    ):
        """Initialize the SimpleTagger object.

           Args:
               attribute (str): The name of the attribute that will hold the tag.
                   this attribute will be accessible through the attribute
                   `._` of Token objects. Example `token_object._.<attribute>
               lookups (set, list or dict): If of type `list` of `set`, it should contain
                   the tokens that are to be searched for and tagged in the Doc 
                   object's text. Example: ['the', 'myself', ...]
                   If of type `dict`, the keys should be the tokens texts to be
                   tagged, and values should hold a single tag for each such token.
                   Example: tagging stop words {'the': True, 'myself' : True}.
               tag (object, optional): If `lookups` is of type `list`, then this
                   will be the tag assigned to all matched tokens. It will be 
                   ignored if `lookups` if of type `dict`.
               default_tag: (object, optional): The default tag to be assigned
                   in case the token text maches no entry in `lookups`.
               case_sensitive: (bool, optional): If set to True, then matching
                   token texts to `lookups` will become case sensitive.
                   Defaults to True.
        """

        self.attribute = attribute

        # Desensitize tokens in lookups if `case_sensitive` is False
        if case_sensitive:
            self.lookups = lookups
        else:
            self.lookups = self._desensitize_lookups(lookups)

        # If `lookups` is a `list`, convert it to a `set`
        self.lookups = (
            set(self.lookups) if isinstance(self.lookups, list) else self.lookups
        )

        self.case_sensitive = case_sensitive
        self.tag = tag
        self.default_tag = default_tag

    def __call__(self, doc: Doc):

        # Start tagging
        for token in doc:

            # Get the tag
            tag = self._get_tag(token)

            # Set the attribute of each matched token to the tag
            token.set_attribute(name=self.attribute, value=tag)

    def _desensitize_lookups(self, lookups: Union[dict, list, set]):
        """Converts every token in `self.lookups` to lower case to enable
           case in-sensitive matching

           Args:
               lookups (set, list or dict): Check out the docstring of `__init__()`.

           Returns:
               A transformed version  of `lookup` where all token texts are in 
               lower case.
 
        """

        # Replace dict keys with lower-case versions
        if isinstance(lookups, dict):
            return {token.lower(): lookups[token] for token in lookups}

        # Convert all list or set elements to lower case
        if isinstance(lookups, list) or isinstance(lookups, set):
            return {token.lower() for token in lookups}

    def _get_tag(self, token: Token):
        """Gets the tag that should be assigned to the Token object `token`.
           If now value is found, self.default is used instead


           Args:
               token (Token): The Token object to which the tag is to be assigned.

           Returns:
               tag (object): Check out the docstring of `__init__()`.
        """

        # Get the token text
        token_text = token.text if self.case_sensitive else token.text.lower()

        # If `self.lookups` is a dict, get the corresponding tag
        if isinstance(self.lookups, dict):

            # Get the associated tag
            tag = self.lookups.get(token_text, self.default_tag)

        # If `self.lookups` is a set, use the `self.tag` attribute.
        elif isinstance(self.lookups, set):

            tag = self.tag if token_text in self.lookups else self.default_tag

        return tag
