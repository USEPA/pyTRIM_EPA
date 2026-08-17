from math import e, log
from .utils import input_units, output_units


# Equation B-1
@input_units(
    Pr='[mass]/[mass]', Pd='[mass]/[mass]', Pv='[mass]/[mass]'
)
@output_units('mg/kg')
def get_c_ag_produce_dw(Pr, Pd, Pv):
    """Equation B-13
    Chemical Concentration in Aboveground Produce

    C_AG-produce-DW(i) = Pr_AG-produce-DW(i) + Pd(i) + Pv(i)

    Where:
    `C_AG-produce-DW`(i)    = Concentration of chemical in edible portion
                              of aboveground produce type i, exposed or
                              protected, on a dry-weight (DW) basis
                              (mg/kg produce DW)
    `Pr`_AG-produce-DW(i)   = Chemical concentration in edible portion
                              of aboveground produce type i, exposed
                              or protected, due to root uptake from soil
                              at the root-zone depth of the produce
                              growing area (mg/kg produce DW)
                              (Equation B-2)
    `Pd`(i)                 = Chemical concentration in edible portion
                              of aboveground produce type i due to
                              deposition of particles (mg/kg produce DW);
                              for protected aboveground produce, Pd equals zero
                              (Equation B-3)
    `Pv`(i)                 = Chemical concentration in edible portion
                              of aboveground produce type i due to air-to-plant
                              transfer (μg/g [or mg/kg] produce DW);
                              for protected aboveground produce, Pv equals zero
                              (Equation B-4)
    """
    return Pr + Pd + Pv


# Equation B-2
@input_units(
    Cs_root_zone='[mass]/[mass]', Br='[mass]/[mass]'
)
@output_units('mg/kg')
def get_pr_ag_produce_dw(Cs_root_zone, Br):
    """Equation B-2
    Chemical Concentration in Aboveground Produce Due to Root Uptake

    Pr_AG-produce-DW(i) = Cs_root-zone_produce(i) * Br_AG-produce-DW(i)

    Where:
    `Pr`_AG-produce-DW(i)       = Concentration of chemical in edible
                                  portion of aboveground produce type i,
                                  exposed or protected, due to root uptake
                                  from soil at root-zone depth in the
                                  produce-growing area, on a dry-weight (DW)
                                  basis (mg/kg produce DW)
    `Cs_root-zone`_produce(i)   = Average chemical concentration in soil
                                  at root-zone depth in produce-growing area
                                  (mg/kg soil DW)
    `Br`_AG-produce-DW(i)       = Chemical-specific plant/soil chemical
                                  bioconcentration factor for edible portion
                                  of aboveground produce type i,
                                  exposed or protected
                                  (g soil DW / g produce DW)
    """
    return Cs_root_zone * Br


# Equation B-3
@input_units(
    Drdp='[mass]/[area]/[time]', Drwp='[mass]/[area]/[time]',
    Fw='', Rp='', kp='1/[time]', Tp='[time]', Yp='[mass]/[area]'
)
@output_units('mg/kg')
def get_pd(Drdp, Drwp, Fw, Rp, kp, Tp, Yp):
    """Equation B-3:
    Chemical Concentration in Aboveground Produce
    Due to Deposition of Particle-phase Chemical

    Pd(i) = (Drdp + (Fw * Drwp)) * Rp(i) * (1 - e**(-kp(i) * Tp(i))) /
            (Yp(i) * kp(i))

    Where:
    `Pd`(i)     = Chemical concentration in aboveground produce type i
                  on a dry-weight (DW) basis due to particle deposition
                  (mg/kg produce DW);
                  set equal to zero for protected aboveground produce
    `Drdp`      = Average annual dry deposition of particle-phase chemical
                  (g/m^2-yr)
    `Fw`        = Fraction of wet deposition that adheres to plant surfaces;
                  0.2 for anions, 0.6 for cations and most organics (unitless)
    `Drwp`      = Average annual wet deposition of particle-phase chemical
                  (g/m^2-yr)
    `Rp`(i)     = Interception fraction of the edible portion of plant type i
                  (unitless)
    `kp`(i)     = Plant surface loss coefficient for plant type i
                  (yr^-1)
    `Tp`(i)     = Length of exposure to deposition in the field per harvest
                  of the edible portion of plant type i (yr)
    `Yp`(i)     = Yield or standing crop biomass of the edible portion
                  of plant type i (kg produce DW/m^2)
    """
    numerator = (Drdp + (Fw * Drwp)) * Rp * (1 - e**(-1 * kp * Tp))
    denominator = Yp * kp

    return numerator / denominator


# Equation B-4
@input_units(
    Ca='[mass]/[volume]', Fv='', Bv_AG='[mass]/[mass]',
    VG_AG='', rho_a='[mass]/[volume]'
)
@output_units('ug/g')
def get_pv(Ca, Fv, Bv_AG, VG_AG, rho_a):
    """Equation B-4:
    Chemical Concentration in Aboveground Produce
    Due to Air-to-Plant Transfer of Vapor-phase Chemical

    Pv(i) = (Ca * Fv * Bv_AG(i) * VG_AG(i)) / rho_a

    Where:
    `Pv`(i)     = Concentration of chemical in edible portion of
                  aboveground produce type i from air-to-plant transfer
                  of vapor-phase chemical on a dry-weight (DW) basis
                  (μg/g produce DW);
                  set equal to zero for protected aboveground produce
    `Ca`        = Average annual total chemical concentration in air (g/m^3)
    `Fv`        = Fraction of airborne chemical in vapor phase (unitless)
    `Bv_AG`(i)  = Air-to-plant biotransfer factor for aboveground
                  produce type i for vapor-phase chemical in air
                  ([mg/g produce DW] / [mg/g air], i.e., g air/ g produce DW)
    `VG_AG`(i)  = Empirical correction factor for aboveground
                  exposed produce type i to address possible overestimate
                  of the diffusive transfer of chemical from the outside
                  to the inside of bulky produce, such as fruit (unitless)
    `rho_a`     = Density of air (g/m^3)
    """
    return (Ca * Fv * Bv_AG * VG_AG) / rho_a


# Equation B-5
@input_units(C_AG_produce_DW='[mass]/[mass]', MAF='')
@output_units('mg/kg')
def convert_c_ag_produce_ww(C_AG_produce_DW, MAF):
    """Equation B-5:
    Conversion of Aboveground Product Chemical Concentration
    from Dry- to Wet-Weight Basis

    C_AG-produce-WW(i) = (C_AG-produce-DW(i) * ((100 - MAF) / 100)

    Where:
    `C-AG-produce-WW`(i)    = Chemical concentration in edible portion of
                              aboveground produce type i on a wet- weight
                              (WW) basis (mg/kg produce WW)
    `C-AG-produce-DW`(i)    = Chemical concentration in edible portion of
                              aboveground produce type i on a dry- weight
                              (DW) basis (mg/kg produce DW)
    `MAF`(i)                = Moisture adjustment factor for aboveground
                              produce type i to convert the chemical
                              concentration estimated for dry-weight
                              produce to the corresponding chemical
                              concentration for full-weight fresh produce
                              (percent water)
    """
    if MAF < 0:
        raise TypeError('MAF cannot be < 0')

    return C_AG_produce_DW * ((100 - MAF) / 100)


# Equation B-6
@input_units(
    Cs_root_zone='[mass]/[mass]', RCF='[volume]/[mass]', VG='',
    Kds='[volume]/[mass]'
)
@output_units('mg/kg')
def get_c_bg_produce_dw_rcf(Cs_root_zone, RCF, VG, Kds):
    """Equation B-6:
    Chemical Concentration in Belowground Produce:
    Nonionic Organic Chemicals

    C_BG-produce-DW = (Cs_root-zone_produce * RCF * VG_rootveg) / Kds

    where:
    `C_BG-produce-DW`       = Concentration of chemical in belowground (BG)
                              produce (i.e., tuber or root vegetable)
                              on a wet-weight (WW) basis
                              (mg chemical/kg produce WW)*
    `Cs_root-zone`_produce  = Average chemical concentration in soil at
                              root-zone depth in produce-growing area,
                              on a dry-weight (DW) basis
                              (mg chemical/kg soil DW)
    `RCF`                   = Chemical-specific root concentration factor
                              for tubers and root produce
                              (L soil pore water/kg root DW)*
    `VG`_rootVeg            = Empirical correction factor for belowground
                              produce (i.e., tuber or root vegetable)
                              to account for possible overestimate of the
                              diffusive transfer of chemicals from
                              the outside to the inside of bulky tubers
                              or roots (based on carrots and potatoes)
                              (unitless)*
    `Kds`                   = Chemical-specific soil/water partition
                              coefficient (L soil pore water/kg soil DW)

    * Note that there is only one type of BG produce;
    hence there are no plant-type-specific subscripts
    """
    return (Cs_root_zone * RCF * VG) / Kds


# Equation B-7
@input_units(Cs_root_zone='[mass]/[mass]', Br='[mass]/[mass]', VG='')
@output_units('mg/kg')
def get_c_bg_produce_dw_br(Cs_root_zone, Br, VG):
    """Equation B-7:
    Chemical Concentration in Belowground Produce:
    Inorganic Chemicals

    C_BG-produce-DW = Cs_root-zone_produce * Br_BG-produce-DW * VG_rootveg

    where:
    `C_BG-produce-DW`       = Concentration of chemical in edible portion
                              of aboveground produce, due to root uptake
                              from soil at root-zone depth in the
                              produce-growing area, on a dry-weight (DW)
                              basis (mg/kg produce DW)
    `Cs_root-zone`_produce  = Average chemical concentration in soil at
                              root-zone depth in produce-growing area
                              (mg/kg soil DW)
    `Br`_BG-produce-DW      = Chemical-specific root/soil chemical
                              bioconcentration factor for edible portion
                              of belowground produce
                              (g soil DW / g produce DW)
    `VG`_rootveg            = Empirical correction factor for belowground
                              produce (as in Equation B-6)
                              (unitless)
    """
    return Cs_root_zone * Br * VG


# Equation B-8
@input_units(C_BG_produce_DW='[mass]/[mass]', MAF='')
@output_units('mg/kg')
def convert_c_bg_produce_ww(C_BG_produce_DW, MAF):
    """Equation B-8:
    Conversion of Belowground Product Chemical Concentration
    from Dry- to Wet-Weight Basis

    C_BG-produce-WW(i) = (C_AG-produce-DW(i) * ((100 - MAF) / 100)

    Where:
    `C-BG-produce-WW`(i)    = Chemical concentration in edible portion of
                              belowground produce on a weight-weight (WW)
                              basis (mg/kg produce WW)
    `C-BG-produce-DW`(i)    = Concentration of chemical in edible portion
                              of belowground produce, due to root uptake
                              from soil at root-zone depth in the
                              produce-growing area, on a dry-weight (DW)
                              basis (mg/kg produce DW)
    `MAF`(i)                = Moisture adjustment factor (as in Equation B-5,
                              but single value for below ground produce)
                              (percent water)
    """
    if MAF < 0:
        raise TypeError('MAF cannot be < 0')

    return (C_BG_produce_DW * ((100 - MAF) / 100))


# Equation B-9
@input_units(
    Ba='[time]/[mass]', MF='', Soil_Ch_Intake='[mass]/[time]',
    Plant_Ch_Intakes='[mass]/[time]'
)
@output_units('mg/kg')
def get_c_mammal(Ba, MF, Soil_Ch_Intake, Plant_Ch_Intakes):
    """Equation B-9
    Chemical Concentration in Beef, Pork, or Total Dairy

    C_mammal(m) = Ba(m) * MF * (Soil_Ch_Intake(m) + SUM(Plant_Ch_Intakes(m)))

    Where:
    `C_mammal`(m)           = Concentration of chemical in
                              mammalian animal product m,
                              where m = beef, pork, or total dairy
                              (mg chemical/kg animal product WW)
    `Ba`(m)                 = Chemical-specific biotransfer factor
                              for chemical in diet to chemical
                              in animal food product m,
                              where m = beef, pork, or total dairy
                              ([mg chemical/kg animal product WW] /
                              [mg chemical intake/day] or day/kg WW)
    `MF`                    = Chemical-specific mammalian metabolism factor
                              that accounts for endogenous degradation
                              of the chemical (unitless)
    `Soil_Ch_Intake`(m)     = Incidental ingestion of chemical in surface soils
                              by livestock type m during grazing
                              or consumption of foods placed on the ground
                              (mg/day);
                              see Equation B-11
    `Plant_Ch_Intakes`(m)   = For livestock (animal product) type m,
                              ingestion of chemical from plant feed type i
                              (mg chemical/kg livestock WW);
                              see Equation B-12
                              (If m = beef or total dairy,
                              then n = 3 and i = forage, silage, and grain;
                              m = pork, then n = 2 and i = silage and grain;
                              m = poultry, then n = 1 and i = grain.)
    """
    return Ba * MF * (Soil_Ch_Intake + sum(Plant_Ch_Intakes))


# Equation B-10
@input_units(
    Ba='[time]/[mass]', Soil_Ch_Intake='[mass]/[time]',
    Plant_Ch_Intakes='[mass]/[time]'
)
@output_units('mg/kg')
def get_c_poultry(Ba, Soil_Ch_Intake, Plant_Ch_Intakes):
    """Equation B-10
    Chemical Concentration in Poultry or Eggs

    C_poultry(m) = Ba(m) * (Soil_Ch_Intake(m) + Plant_Ch_Intakes(m))

    Where:
    `C_poultry`(m)          = Concentration of chemical in
                              food product m, where m = poultry or eggs
                              (mg chemical/kg animal product WW)
    `Ba`(m)                 = Chemical-specific biotransfer factor
                              for food product m, where m = poultry or eggs
                              (day/kg animal product WW)
    `Soil_Ch_Intake`(m)     = Incidental ingestion of chemical in surface soils
                              by consumption of food on the ground
                              (mg chemical/day) where m = poultry;
                              see Equation B-11
    `Plant_Ch_Intakes`(m)   = For poultry (and eggs), animal m,
                              ingestion of the chemical in plant feed types
                              (mg chemical/day), which for poultry
                              are limited to grain;
                              see Equation B-12
    """
    return Ba * (Soil_Ch_Intake + Plant_Ch_Intakes)


# Equation B-11
@input_units(Qs='[mass]/[time]', Cs_s='[mass]/[mass]', Bs='')
@output_units('mg/day')
def get_soil_ch_intake(Qs, Cs_s, Bs):
    """Equation B-11
    Incidental Ingestion of Chemical in Soil by Livestock

    Soil_Ch-Intake(m) = Qs(m) * Cs_s-livestock * Bs

    Where:
    `Soil_Ch-Intake`(m) = Incidental ingestion of the chemical
                          in surface soils by livestock type m
                          during grazing or consumption of foods
                          placed on the ground (mg chemical/day)
    `Qs`(m)             = Quantity of soil eaten by animal type m
                          each day (kg soil DW/day)
    `Cs_s`-livestock    = Chemical concentration in surface soil
                          in contaminated area where livestock feed
                          (mg chemical/kg soil DW)
    `Bs`                = Soil bioavailability factor for livestock (unitless)
                          (assumed to be the same for birds and mammals)
    """
    return Qs * Cs_s * Bs


# Equation B-12
@input_units(F='', Qp='[mass]/[time]', C='[mass]/[mass]')
@output_units('mg/day')
def get_plant_ch_intake(F, Qp, C):
    """Equation B-12
    Ingestion of Chemical in Feed by Livestock

    Plant_Ch-Intake(i, m) = F(i, m) * Qp(i, m) * C_feed(i)

    Where:
    `Plant_Ch-Intake`(i, m) = Ingestion of chemical in plant feed type i
                              (mg chemical/day),
                              where i = forage, silage, or grain,
                              for livestock type m
    `F`(i, m)               = Fraction of plant feed type i obtained
                              from contaminated area used to grow animal feed,
                              where i = forage, silage, or grain (unitless)
                              for livestock type m
    `Qp`(i, m)              = Quantity of plant feed type i consumed per animal
                              per day (kg plant feed DW/day),
                              where i = forage, silage, or grain,
                              for livestock type m
    `C`_feed(i)             = Concentration of chemical in ingested plant
                              feed type i (mg chemical/kg plant feed DW),
                              where i = forage, silage, or grain
    """
    return F * Qp * C


# Equation B-13
@input_units(
    Pr='[mass]/[mass]', Pd='[mass]/[mass]', Pv='[mass]/[mass]'
)
@output_units('mg/kg')
def get_c_feed(Pr, Pd, Pv):
    """Equation B-13
    Chemical Concentration in Livestock Feed (All Aboveground)

    C_feed(i) = Pr_feed(i) + Pd(i) + Pv(i)

    Where:
    `C_feed`(i)     = Concentration of chemical in plant feed type i
                      on a dry-weight (DW) basis
                      (mg chemical/kg plant feed DW),
                      where i = forage, silage, or grain
    `Pr`_feed(i)    = Concentration of chemical in plant feed type i
                      due to root uptake from soil (mg/kg DW),
                      where i = forage, silage, or grain;
                      see Equation B-14
    `Pd`(i)         = Concentration of chemical in plant feed type i
                      due to wet and dry deposition of particle-phase chemical
                      (mg/kg DW), where i = forage, silage, or grain;
                      when i = grain, the Pd term equals zero
    `Pv`(i)         = Concentration of chemical in plant feed type i
                      due to air-to-plant transfer of vapor-phase chemical
                      (μg/g [or mg/kg] DW) where i = forage, silage, or grain;
                      when i = grain, the Pd term equals zero
    """
    return get_c_ag_produce_dw(Pr, Pd, Pv)


# Equation B-14
@input_units(Cs_root_zone='[mass]/[mass]', Br='[mass]/[mass]')
@output_units('mg/kg')
def get_pr_feed(Cs_root_zone, Br):
    """Equation B-14
    Chemical Concentration in Livestock Feed Due to Root Uptake

    Pr_feed(i) = Cs_root-zone_feed(i) * Br_feed(i)

    Where:
    `Pr`_feed(i)            = Concentration of chemical in plant feed type i
                              due to root uptake from soil on a dry-weight (DW)
                              basis (mg chemical/kg plant feed DW),
                              where i = forage, silage, or grain
    `Cs_root-zone`_feed(i)  = Average chemical concentration in soil
                              at root-zone depth in area used to grow
                              plant feed type i (mg chemical/kg soil DW),
                              where i = forage, silage, or grain
    `Br`_feed(i)            = Chemical-specific plant-soil bioconcentration
                              factor for plant feed type i
                              (kg soil DW/kg plant feed DW),
                              where i = forage, silage, or grain
    """
    return get_pr_ag_produce_dw(Cs_root_zone, Br)


# Equation B-39
@input_units(
    C_milkfat='[mass]/[mass]', f_mbm='', C_aqueous='[mass]/[mass]',
    IR_milk='[mass]/[time]', AE_inf='',
    ED='[time]', BW_inf='[mass]', AT='[time]'
)
@output_units('mg/kg/day')
def get_average_daily_dose_to_nursing_infant(
    C_milkfat, f_mbm, C_aqueous, IR_milk, AE_inf, ED, BW_inf, AT=None
):
    """Equation B-39
    Average Daily Dose of Chemical to the Nursing Infant

    DAI_inf = floor((C_milkfat * f_mbm) + (C_aquaeous * (1 - f_mbm))) *
              IR_milk * AE_inf * ED / (BW_inf * AT)

    Where:
    `DAI_inf`   = Average daily dose of chemical absorbed by infant
                  (mg chemical/kg body weight-day)
    `C_milkfat` = Concentration of chemical in lipid phase of maternal milk
                  (mg chemical/kg milk lipid;
                  calculated using Equation B-40)
    `f_mbm`     = Fraction of fat in breast milk (unitless)
    `C_aqueous` = Concentration of chemical in aqueous phase of maternal milk
                  (mg chemical/kg aqueous phase milk;
                  calculated using Equation B-44)
    `IR_milk`   = Infant milk ingestion rate over the duration of nursing
                  (kg milk/day)
    `AE_inf`    = Absorption efficiency of the chemical
                  by the oral route of exposure
                  (i.e., chemical-specific fraction of ingested chemical
                  that is absorbed by the infant) (unitless)
    `ED`        = Exposure duration, i.e., duration of breast feeding (days)
    `BW_inf`    = Body weight of infant averaged over
                  the duration of nursing (kg)
    `AT`        = Averaging time associated with exposure of interest;
                  equal to ED (days)
    """

    AT = AT or ED

    numerator = (
        (C_milkfat * f_mbm) + (C_aqueous * (1 - f_mbm))
    ) * IR_milk * AE_inf * ED

    denominator = BW_inf * AT

    return numerator / denominator


# Equation B-40
@input_units(
    DAI_mat='[mass]/[time]/[mass]',  # mg/kg-day = mg/day/kg
    f_f='[mass]/[mass]', k_elim='1/[time]',
    f_fm='', k_fat_elac='1/[time]', t_bf='[time]', t_pn='[time]'
)
@output_units('mg/kg')
def get_pr_breastmilk_fat(
    DAI_mat, f_f, k_elim, f_fm, k_fat_elac, t_bf, t_pn
):
    """Equation B-40
    Chemical Concentration in Breast Milk Fat

    C_milkfat = (DAI_mat * f_f) / (k_elim * f_fm) * (
                    (k_elim / k_fat_elac) + (
                        (1 / (k_fat_elac * t_bf)) *
                        (1 - e**(-k_elim * t_pn) - (k_elim / k_fat_elac)) *
                        (1 - e**(-k_fat_elac * t_bf))
                    )
                )

    Where:
    `C_milkfat`     = Concentration of chemical in lipid phase of maternal milk
                      (mg chemical/kg lipid)
    `DAI_mat`       = Daily absorbed maternal chemical dose
                      (mg chemical/kg maternal body weight-day;
                      calculated using Equation B-41)
    `f_f`           = Fraction of total maternal body burden of chemical
                      that is stored in maternal fat
                      (mg chemical in body fat/mg total chemical in whole body;
                      value from literature or EPA default -
                      see Section B.6.5 of Appendix B)
    `k_elim`        = Chemical-specific total elimination rate constant
                      for elimination of the chemical by non-lactating women
                      (per day; e.g., via urine, bile to feces, exhalation;
                      value from literature or calculated using Equation B-42)
    `f_fm`          = Fraction of maternal body weight that is fat stores
                      (unitless)
    `k_fat_elac`    = Chemical-specific rate constant for total elimination
                      of chemical in the lipid phase of milk during nursing
                      (per day; value from literature
                      or calculated using Equation B-43)
    `t_bf`          = Duration of breast feeding (days)
    `t_pn`          = Duration of mother’s exposure prior to parturition
                      and initiation of breast feeding (days)
    """
    return (
        (DAI_mat * f_f) / (k_elim * f_fm) * (
            (k_elim / k_fat_elac) + (
                (1 / (k_fat_elac * t_bf)) *
                (1 - e**(-k_elim * t_pn) - (k_elim / k_fat_elac)) *
                (1 - e**(-k_fat_elac * t_bf))
            )
        )
    )


# Equation B-41
@input_units(
    ADD_adult='[mass]/[time]/[mass]',  # mg/kg-day = mg/day/kg
    AE_mat=''
)
@output_units('mg/kg/day')
def get_maternal_intake(ADD_adult, AE_mat):
    """Equation B-41
    Daily Maternal Absorbed Intake

    DAI_mat = ADD_adult * AE_mat

    Where:
    `DAI_mat`       = Daily maternal dose of chemical
                      absorbed from medium i (mg/kg-day)
    `ADD_adult`    = Average daily dose to the mother (mg/kg-day)
                      (see Section B.3.3 of Appendix B, Equation B-37)
    `AE_mat`        = Absorption efficiency of the chemical
                      by the oral exposure route
                      (i.e., chemical-specific fraction of ingested chemical
                      that is absorbed) by the mother (unitless)
    """
    return ADD_adult * AE_mat


# Equation B-42
@input_units(h='[time]')
@output_units('day^-1')
def get_biolgical_elimination_rate_nonlactating(h):
    """ Equation B-42
    Biological Elimination Rate Constant for Chemicals for Non-Lactating Women

    k_elim = ln(2) / h

    Where:
    `k_elim`    = Chemical-specific elimination rate constant
                  for elimination of the chemical for non-lactating women
                  (per day; e.g., via urine, bile to feces, exhalation)
    `ln(2)      = Natural log of 2 (unitless constant)
    `h`         = Chemical-specific biological half-life of chemical
                  for non-lactating women (days)
    """
    return log(2) / h


# Equation B-43
@input_units(
    k_elim='1/[time]', IR_milk='[mass]/[time]',
    f_f='[mass]/[mass]', f_mbm='', f_fm='', BW_mat='[mass]'
)
@output_units('day^-1')
def get_biolgical_elimination_rate_lactating(
    k_elim, IR_milk, f_f, f_mbm, f_fm, BW_mat
):
    """ Equation B-43
    Biological Elimination Constant for Lipophilic Chemicals
    for Lactating Women

    k_fat_elac = k_elim + ((IR_milk * f_f * f_mbm) / (f_fm * BW_mat))

    Where:
    `k_fat_elac`    = Rate constant for total elimination of chemical
                      during nursing (per day);
                      accounts for both elimination by adults in general
                      and the additional chemical elimination
                      via the lipid phase of milk in nursing women
    `k_elim`        = Elimination rate constant for chemical from adults,
                      including non-lactating women
                      (per day; e.g., via urine, bile to feces, exhalation;
                      chemical-specific; value from literature
                      or calculated from half-life using Equation B-42)
    `IR_milk`       = Infant milk ingestion rate over the duration of nursing
                      (kg/day)
    `f_f`           = Fraction of total maternal body burden of chemical
                      that is stored in maternal fat
                      (mg chemical in body fat / mg chemical total in body;
                      value from literature or EPA default)
    `f_mbm`         = Fraction of fat in breast milk (unitless)
    `f_fm`          = Fraction of maternal body weight that is fat stores
                      (unitless)
    `BW_mat`        = Maternal body weight over the entire duration
                      of the mother’s exposure to the chemical
                      including during pregnancy and lactation (kg)
    """
    return k_elim + ((IR_milk * f_f * f_mbm) / (f_fm * BW_mat))


# Equation B-44
@input_units(
    DAI_mat='[mass]/[time]/[mass]',  # mg/kg-day = mg/day/kg
    f_pl='', Pc_bm='', k_aq_elac='1/[time]', f_pm=''
)
@output_units('mg/kg')
def get_pr_aqueous_breastmilk(DAI_mat, f_pl, Pc_bm, k_aq_elac, f_pm):
    """ Equation B-44
    Chemical Concentration in Aqueous Phase of Breast Milk

    C_aqueous = (DAI_mat * f_pl * Pc_bm) / (k_aq_elac * f_pm)

    Where:
    `C_aqueous` = Concentration of chemical in aqueous phase
                  of maternal milk (mg/kg)
    `DAI_mat`   = Daily absorbed maternal chemical dose
                  (mg/kg-day; calculated by Equation B-41)
    `f_pl`      = Fraction of chemical in the body (based on absorbed intake)
                  that is in the blood plasma compartment
                  (unitless; value from literature
                  or calculated by Equation B-45)
    `Pc_bm`     = Partition coefficient for chemical
                  between the plasma and breast milk in the aqueous phase
                  (unitless); assumed to equal 1.0
    `k_aq_elac` = Chemical-specific rate constant
                  for total elimination of chemical
                  in the aqueous phase of milk during nursing
                  (per day; value from literature
                  or calculated in Equation B-46)
    `f_pm`      = Fraction of maternal weight that is blood plasma (unitless)
    """
    return (DAI_mat * f_pl * Pc_bm) / (k_aq_elac * f_pm)


# Equation B-45
@input_units(f_bl='', f_bp='', Pc_RBC='')
@output_units('')
def get_fraction_blood_plasma(f_bl, f_bp, Pc_RBC):
    """Equation B-45
    Fraction of Total Chemical in Body in the Blood Plasma Compartment

    f_pl = (f_bl * f_bp) / (f_bp + (Pc_RBC * (1 - f_bp)))

    Where:
    `f_pl`      = Fraction of chemical in body (based on absorbed intake)
                  that is in the blood plasma compartment
                  (unitless); chemical-specific
    `f_bl`      = Fraction of chemical in body (based on absorbed intake)
                  in the whole blood compartment
                  (unitless); chemical-specific
    `f_bp`      = Fraction of whole blood that is plasma (unitless)
    `Pc_RBC`    = Partition coefficient for chemical
                  between red blood cells and plasma
                  (unitless); chemical-specific
    """
    return (f_bl * f_bp) / (f_bp + (Pc_RBC * (1 - f_bp)))


# Equation B-46
@input_units(k_elim='1/[time]')
@output_units('day^-1')
def get_biological_elim_rate_hydrophilic_chem(k_elim):
    """Equation B-46
    Biological Elimination Rate Constant for Hydrophilic Chemicals

    k_aq_elac = k_elim

    `k_aq_elac`  = Chemical-specific rate constant
                  for total elimination of chemical by lactating women
                  for hydrophilic chemicals (per day)
    `k_elim`    = Chemical-specific rate constant
                  for total elimination of chemical by non-lactating women
                  (per day; e.g., via urine, bile to feces, exhalation;
                  value from literature
                  or calculated from half-life using Equation B-42)
    """
    return k_elim


# Equation B-47
@input_units(DAI_mat_MeHg='[mass]/[time]/[mass]')  # mg/kg-day = mg/day/kg
@output_units('mg/kg/day')
def get_infant_daily_dose_methyl_mercury(DAI_mat_MeHg):
    """Equation B-47
    Calculation of Infant Average Daily Absorbed Dose of Methyl Mercury

    DAI_inf_MeHg = DAI_mat_MeHg

    `DAI_inf_MeHg`  = Average daily dose of MeHg absorbed by infant
                      from breast milk (mg/kg-day)
    `DAI_mat_MeHg`  = Average daily dose of methyl
    """
    return DAI_mat_MeHg
