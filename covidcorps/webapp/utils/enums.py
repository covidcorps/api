from enum import Enum
from typing import List

class ChoicesEnum(Enum):
    @classmethod
    def choices(cls):
        return [(tag.name, tag.value) for tag in cls]

class USStates(ChoicesEnum):
    AL = "Alabama"
    AK = "Alaska"
    AZ = "Arizona"
    AR = "Arkansas"
    CA = "California"
    CO = "Colorado"
    DC = "District of Columbia"
    NC = "North Carolina"
    CT = "Connecticut"
    DE = "Delaware"
    FL = "Florida"
    GA = "Georgia"
    HI = "Hawaii"
    ID = "Idaho"
    IL = "Illinois"
    IN = "Indiana"
    IA = "Iowa"
    KS = "Kansas"
    KY = "Kentucky"
    LA = "Louisiana"
    ME = "Maine"
    MD = "Maryland"
    MA = "Massachusetts"
    MI = "Michigan"
    MN = "Minnesota"
    MS = "Mississippi"
    MO = "Missouri"
    MT = "Montana"
    NE = "Nebraska"
    NV = "Nevada"
    NH = "New Hampshire"
    NJ = "New Jersey"
    NM = "New Mexico"
    NY = "New York"
    ND = "North Dakota"
    OH = "Ohio"
    OK = "Oklahoma"
    OR = "Oregon"
    PA = "Pennsylvania"
    RI = "Rhode Island"
    SC = "South Carolina"
    SD = "South Dakota"
    TN = "Tennessee"
    TX = "Texas"
    UT = "Utah"
    VT = "Vermont"
    VA = "Virginia"
    WA = "Washington"
    WV = "West Virginia"
    WI = "Wisconsin"
    WY = "Wyoming"

class CorpsMemberStatus(ChoicesEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class AssignmentStatus(ChoicesEnum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    ENROUTE = "ENROUTE"
    ONSITE = "ONSITE"
    COMPLETE = "COMPLETE"

class CorpsMemberCategories(ChoicesEnum):
    DOCTOR = "Doctor"
    NURSE = "Nurse"
    RESPIRATORY = "Respiratory Specialist"
    ORDERLY = "Orderly"
    PA = "Physicians Assistant"
    NP = "Nurse Practicioner"
    PSYCHOLOGIST = "Psychologist"
    PSYCHIATRIST = "Psychiatrist"