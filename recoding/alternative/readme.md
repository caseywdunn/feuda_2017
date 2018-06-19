# Alternative randomized recoding

The goal of these analyses is to examine the general impact of recoding
character states to reduced alphabets on posterior predictive scores.

## Methods

    python alt_recode.py WhelanD20_AA.phy 4 > alt_recode.log
    sbatch phylobayesmpi_batch.sh

### Codings

The SR6 codings are from the left side of Table 1 of https://academic.oup.com/mbe/article-lookup/doi/10.1093/molbev/msm144 :

    ADEGKNPQRSTCFHILMVWY
    ADEGKNPQRST CFHILMVWY
    ADEGNPST CHKQRW FILMVY
    AGNPST CHWY DEKQR FILMV
    AGPST CFWY DEN HKQR ILMV
    APST CW DEGN FHY ILMV KQR
    AGST CW DEN FY HP ILMV KQR
    AST CG DEN FY HP ILV KQR MW
    AST CW DE FY GN HQ ILV KR MP
    AST CW DE FY GN HQ IV KR LM P
    AST C DE FY GN HQ IV KR LM P W
    AST C DE FY G HQ IV KR LM N P W
    AST C DE FY G H IV KR LM N P Q W
    AST C DE FL G H IV KR M N P Q W Y
    AST C DE F G H IV KR L M N P Q W Y
    AT C DE F G H IV KR L M N P Q S W Y
    AT C DE F G H IV K L M N P Q R S W Y
    A C DE F G H IV K L M N P Q R S T W Y
    A C D E F G H IV K L M N P Q R S T W Y
    A C D E F G H I V K L M N P Q R S T W Y
