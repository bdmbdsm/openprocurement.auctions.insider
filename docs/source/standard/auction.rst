.. . Kicking page rebuild 2014-10-30 17:00:08
.. include:: defs.hrst

.. index:: Auction, Auction
.. _auction:

Auction
=======

Schema
------

:id:
   uuid, auto-generated, read-only

   Internal identification of the procedure.

:date:
   :ref:`date`, auto-generated, read-only

   The date of the procedure creation/undoing.

:owner:
   string, auto-generated, read-only

   The entity (eMall) whom the procedure has been created by.

:auctionParameters:
   :ref:`auctionParameters`

   Aditional auction parameters/

:title:
   string, multilingual, required

   Can be edited during the rectificationPeriod.
    
   * Ukrainian by default (required) - Ukrainian title
    
   * ``title_en`` (English) - English title
    
   * ``title_ru`` (Russian) - Russian title
    
   Oprionally can be mentioned in English/Russian.

   The name of the auction, displayed in listings. 

:description:
   string, multilingual, required

   Can be edited during the rectificationPeriod.
    
   |ocdsDescription|
   A description of the goods, services to be provided.
    
   * Ukrainian by default - Ukrainian decription
   
   * ``decription_en`` (English) - English decription
   
   * ``decription_ru`` (Russian) - Russian decription

:dgfDecisionID:
   string, required

   Can be edited during the rectificationPeriod.

   The number of the decision.

:dgfDecisionDate:
   string, required

   Can be edited during the rectificationPeriod.

   The date of the decision on the approval of the terms of sale.

:procurementMethod:
   string, auto-generated, read-only

   Purchase method. The only value is “open”.

:auctionID:
   string, auto-generated, read-only

   The auction identifier to refer auction to in "paper" documentation. 

   |ocdsDescription|
   AuctionID should always be the same as the OCID. It is included to make the flattened data structure more convenient.

:dgfID:
   string, required

   Can be edited during the rectificationPeriod.
    
   Identification number of the auction (also referred to as `lot`) in the XLS of Deposit Guarantee Fund.
    
:procurementMethodType:
    string, required
    
    The type of the procedure. The suitable value is `dgfInsider`. 

:procurementMethodDetails:
   string, optional

   Parameter that accelerates auction periods. Set quick, accelerator=1440 as text value for procurementMethodDetails for the time frames to be reduced in 1440 times.

:submissionMethod:
   string, auto-generated, read-only

   The given value is `electronicAuction`.

:awardCriteria:
   string, auto-generated, read-only

   Сriterion of a winner selection. The given value is `highestCost`.

:procuringEntity:
   :ref:`ProcuringEntity`, required

   Organization conducting the auction.
   

   |ocdsDescription|
   The entity managing the procurement, which may be different from the buyer who is paying / using the items being procured.

:tenderAttempts:
   integer, required

   Can be edited during the rectificationPeriod.

   The number which represents what time (from 1 up to 8) auction is taking place.

:value:
   :ref:`value`, required

   Auction starting price.

   |ocdsDescription|
   The total estimated value of the procurement.

:guarantee:
   :ref:`Guarantee`, required

   Can be edited during the rectificationPeriod. `guarantee.amount` can not be greater than `value.amount`.

   The assumption of responsibility for payment of performance of some obligation if the liable party fails to perform to expectations.

:items:
   Array of :ref:`item` objects, required

   Can be edited during the rectificationPeriod (Can editing in 2 ways: each object from the array separately and the entire array together).

   List that contains single item being sold. 

   |ocdsDescription|
   The goods and services to be purchased, broken into line items wherever possible. Items should not be duplicated, but a quantity of 2 specified instead.

:features:
   Array of :ref:`Feature` objects

   Features of auction.

:documents:
   Array of :ref:`document` objects
 
   |ocdsDescription|
   All documents and attachments related to the auction.

:dateModified:
   :ref:`date`, auto-generated, read-only

   |ocdsDescription|
   Date when the auction was last modified

:questions:
   Array of :ref:`question` objects

   Questions to ``procuringEntity`` and answers to them.

:bids:
   Array of :ref:`bid` objects

   A list of all bids placed in the auction with information about participants, their proposals and other qualification documentation.

   |ocdsDescription|
   A list of all the companies who entered submissions for the auction.

:minimalStep:
   :ref:`value`, required

   Can be edited during the rectificationPeriod. `minimalStep.amount` can not be greater than `value.amount`.

   Auction step (increment). Validation rules:

   * `amount` should be greater than `Auction.value.amount`
   * `currency` should either be absent or match `Auction.value.currency`
   * `valueAddedTaxIncluded` should either be absent or match `Auction.value.valueAddedTaxIncluded`

:awards:
    Array of :ref:`award` objects

    All qualifications (disqualifications and awards).

:contracts:
    Array of :ref:`Contract` objects

    |ocdsDescription|
    Information on contracts signed as part of a process.

:rectificationPeriod:
   :ref:`period`, auto-generated, read-only

   The time span during which the owner can edit some data within the procedure.

:enquiryPeriod:
   :ref:`period`, auto-generated, read-only

   Period when questions are allowed.

   |ocdsDescription|
   The period during which enquiries may be made and will be answered.

:tenderPeriod:
   :ref:`period`, auto-generated, read-only

   Period when bids can be submitted.

   |ocdsDescription|
   The period when the auction is open for submissions. The end date is the closing date for auction submissions.

:auctionPeriod:
   :ref:`period`, required

   Period when Auction is conducted. `startDate` should be provided.

:auctionUrl:
    url, auto-generated, read-only

    A web address where auction is accessible for view.

:awardPeriod:
   :ref:`period`, auto-generated, read-only

   Awarding process period.

   |ocdsDescription|
   The date or period on which an award is anticipated to be made.

:status:
   string, required

   :`active.tendering`:
       Tendering period (tendering)
   :`active.auction`:
       Auction period (auction)
   :`active.qualification`:
       Winner qualification (qualification)
   :`active.awarded`:
       Standstill period (standstill)
   :`unsuccessful`:
       Unsuccessful auction (unsuccessful)
   :`complete`:
       Complete auction (complete)
   :`cancelled`:
       Cancelled auction (cancelled)

   Auction status.

:eligibilityCriteria:
   string, auto-generated, read-only

   Required for `dgfFinancialAssets` procedure.
    
   This field is multilingual: 
    
   * Ukrainian by default - До участі допускаються лише ліцензовані фінансові установи.
    
   * ``eligibilityCriteria_ru`` (Russian) - К участию допускаются только лицензированные финансовые учреждения.
    
   * ``eligibilityCriteria_en`` (English) - Only licensed financial institutions are eligible to participate.

:cancellations:
   Array of :ref:`cancellation` objects.

   Contains 1 object with `active` status in case of cancelled Auction.

   The :ref:`cancellation` object describes the reason of auction cancellation and contains accompanying
   documents  if there are any.

:revisions:
   Array of :ref:`revision` objects, auto-generated

   Historical changes to `Auction` object properties.

:numberOfBids:
   integer, auto-generated, read-only

   Represents the number of submitted bids.

.. _auctionParameters:

auctionParameters
=================

:type:
   string, auto-generated, read-only

   Type of the auction.

:dutchSteps:
   integer, optional

   Number of steps within the Dutch auction phase.
