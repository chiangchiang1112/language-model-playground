r"""Dataset base class."""


from typing import ClassVar, Iterator, List, Optional

import torch.utils.data


class BaseDset(torch.utils.data.Dataset):
    r"""Dataset base class.

    Parameters
    ==========
    ver: str, optional
        Version of the dataset.
        If ``ver is None``, then use default version ``self.__class__.df_ver``
        of the dataset.

    Attributes
    ==========
    df_ver: ClassVar[str]
        Default version of the dataset.
    dset_name: ClassVar[str]
        Display name for dataset on CLI.
        Used for command line argument parsing.
        Subclass must overwrite ``dset_name`` attribute.
    lang: ClassVar[str]
        Language of the dataset.
    spls: Sequence[str]
        All samples in the dataset.
    ver: str
        Version of the dataset.
    vers: ClassVar[List[str]]
        All available version of the dataset.
        Used to check whether specified version ``ver`` is available.

    Raises
    ======
    TypeError
        When ``ver`` is not and instance of ``str``.
    ValueError
        When dataset version ``ver`` is not available.
    """
    # Dataset version, you need to assign a version here, like: 'train', 'test'..., to persent which dataset you want to use
    df_ver: ClassVar[str] = ''
    # Dataset name, like: 'chinese-poem', 'wikitext-2'
    dset_name: ClassVar[str] = 'base'
    # Dataset language, like: 'zh', 'en'
    lang: ClassVar[str] = ''
    # Every version of dataset, 'wikitext-2' has 'train', 'test', 'vaild', three version, it will be a list
    vers: ClassVar[List[str]] = []

    def __init__(self, *, ver: Optional[str] = None):
        super().__init__()
        # Use default version of the dataset.
        if ver is None:
            ver = self.__class__.df_ver
        # Type check.
        elif not isinstance(ver, str):
            raise TypeError('`ver` must be an instance of `str`.')
        elif ver not in self.__class__.vers:
            raise ValueError(
                f'Version {ver} is not available.\n'
                + 'Available versions:\n'
                + ''.join(map(lambda ver: f'\t- {ver}\n', self.__class__.vers))
            )

        self.spls: List[str] = []
        self.ver = ver

    def __iter__(self) -> Iterator[str]:
        r"""Iterate through each sample in the dataset.

        Yields
        ======
        str
            Each text sapmle in ``self.spls``.
        """
        for spl in self.spls:
            yield spl

    def __len__(self) -> int:
        r"""Get dataset size.

        Returns
        =======
        int
            Number of samples in the dataset.
        """
        return len(self.spls)

    def __getitem__(self, idx: int) -> str:
        r"""Sample text using index.

        Parameters
        ==========
        idx: int
            Sample index.

        Raises
        ======
        IndexError
            When ``idx >= len(self.spls)``.
        TypeError
            When ``idx`` is not an instance of ``int``.
        """
        # Type check.
        if not isinstance(idx, int):
            raise TypeError('`idx` must be an instance of `int`.')

        return self.spls[idx]
