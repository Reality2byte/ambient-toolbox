import warnings

import nh3


class BleacherMixin:
    """
    Removes HTML tags and attributes from the fields defined in :py:attr:`BLEACH_FIELD_LIST`.
    Allowed tags and attributes are defined in the :py:attr:`ALLOWED_TAGS` and :py:attr:`ALLOWED_ATTRIBUTES` attributes.
    If :py:attr:`ALLOWED_TAGS` and :py:attr:`ALLOWED_ATTRIBUTES` are not specified on a model a set of default value is
    used:

    ALLOWED_TAGS:
      * span
      * p
      * h1
      * h2
      * h3
      * h4
      * h5
      * h6
      * img
      * div
      * u
      * br
      * blockquote

    ALLOWED_ATTRIBUTES:
      * all tags: class, style, id
      * a: href, rel
      * img: alt, src
    """

    BLEACH_FIELD_LIST: list[str] = []

    DEFAULT_ALLOWED_ATTRIBUTES: dict[str, set[str]] = {
        **nh3.ALLOWED_ATTRIBUTES,
        "*": ("class", "style", "id"),
    }

    DEFAULT_ALLOWED_TAGS: list[str] = [
        *nh3.ALLOWED_TAGS,
        "span",
        "p",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "img",
        "div",
        "u",
        "br",
        "blockquote",
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields_to_bleach = getattr(self, "BLEACH_FIELD_LIST", [])
        self.allowed_tags = set(getattr(self, "ALLOWED_TAGS", self.DEFAULT_ALLOWED_TAGS))
        self.allowed_attributes = getattr(self, "ALLOWED_ATTRIBUTES", self.DEFAULT_ALLOWED_ATTRIBUTES)

        for tag, attribute_list in self.allowed_attributes.items():
            if isinstance(attribute_list, (list, tuple)):
                self.allowed_attributes[tag] = set(attribute_list)
                warnings.warn(
                    "Please use a set instead of a list or tuple for the BleacherMixin.ALLOWED_ATTRIBUTES attribute.",
                    category=DeprecationWarning,
                    stacklevel=1,
                )

    def _bleach_field(self, field_name):
        str_to_bleach = getattr(self, field_name, "")
        if str_to_bleach:
            cleaned_value = nh3.clean(
                str_to_bleach,
                tags=self.allowed_tags,
                attributes=self.allowed_attributes,
            )
            setattr(self, field_name, cleaned_value)

    def save(self, *args, **kwargs):
        for field in self.fields_to_bleach:
            self._bleach_field(field)

        super().save(*args, **kwargs)
