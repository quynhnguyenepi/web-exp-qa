/**
 * Sample Flag Test Script
 *
 * This is an example of a generated Cypress test script for the Flag product.
 * It demonstrates the correct patterns for:
 * - Flag-specific account creation (cy.createFlagsAccount)
 * - saveGeneratedTimeBasedIdAs for dynamic naming
 * - FlagTag import and usage
 * - beforeEach/afterEach hooks (tests are independent)
 * - CommonBasePage for shared utilities
 * - Fluent API chaining with page objects
 */

/* eslint-disable no-undef */
import CommonBasePage from '../../../../pages/common/CommonBasePage';
import FlagsListPage from '../../../../pages/flag/flags/FlagsListPage';
import FlagsPage from '../../../../pages/flag/flags/FlagsPage';
import CommonTag, { FlagTag } from '../../../../support/resources/tagList';

const commonBasePage = new CommonBasePage();
const flagsListPage = new FlagsListPage();
const flagsPage = new FlagsPage();
const variationsTab = flagsPage.variationsTab;

describe(
  'Flag variation management',
  { tags: [FlagTag.flags, CommonTag.smoke_suite, CommonTag.variations] },
  function () {
    //#region Setup Test Data
    beforeEach(function () {
      cy.createFlagsAccount()
        .saveGeneratedTimeBasedIdAs('flagName')
        .saveGeneratedTimeBasedIdAs('variationName1')
        .saveGeneratedTimeBasedIdAs('variationName2')
        .then(function () {
          cy.createFlag(this.flagName);
        })
        .then(() => {
          cy.createVariation(
            this.variationName1,
            this.flagName
          ).createVariation(this.variationName2, this.flagName);
        })
        .then(() => {
          cy.visitProject();
          commonBasePage.waitForTableLoadSpinnerDisappear();
          flagsListPage.openAFlag(this.flagName);
          flagsPage.openVariationsTab();
        });
    });
    //#endregion

    //#region Cleanup
    afterEach(function () {
      cy.deleteAccount();
    });
    //#endregion

    //#region Test Execution
    it('[APPX-5570][Flag][Variations]_Delete variation not used in any rules', function () {
      variationsTab
        .deleteAVariationOnTheTable(this.variationName1)
        .verifyDeletedVariation(this.variationName1)
        .saveAVariation()
        .verifyVariationIsNotDisplayed(this.variationName1);
    });

    it('[APPX-5571][Flag][Variations]_Delete and revert variation', function () {
      variationsTab
        .deleteAVariationOnTheTable(this.variationName1)
        .verifyDeletedVariation(this.variationName1)
        .revertVariation()
        .verifyVariationIsVisible(this.variationName1);
    });

    it('[APPX-5572][Flag][Variations]_Delete and undo variation deletion', function () {
      variationsTab
        .deleteAVariationOnTheTable(this.variationName2)
        .undoDeletionOfVariation()
        .verifyVariationIsVisible(this.variationName2);
    });
    //#endregion
  }
);
