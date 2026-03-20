/**
 * Sample Web Test Script
 *
 * This is an example of a generated Cypress test script for the Web product.
 * It demonstrates the correct patterns for:
 * - Import paths from a typical web regression test location
 * - Builder pattern usage for test data setup
 * - Page object pattern for UI interactions
 * - API-first setup in before() hook
 * - Proper test naming convention
 * - Cleanup in after() hook
 * - Region comments for code organization
 * - Tag usage from tagList.js
 */

/* eslint-disable no-undef */
import ExperimentListPage from '../../../../../pages/web/optimizations/ExperimentListPage';
import ExperimentBuilder from '../../../../../support/builders/web/experiment/experimentBuilder';
import PageBuilder from '../../../../../support/builders/web/pageBuilder';
import WebLeftSideBar from '../../../../../pages/web/experiment_details/WebLeftSideBar';
import VariationsTab from '../../../../../pages/web/experiment_details/VariationsTab';
import CommonTag, { WebTag } from '../../../../../support/resources/tagList';
import referenceData from '../../../../../support/resources/web/referenceData.json';

const experimentListPage = new ExperimentListPage();
const webLeftSideBar = new WebLeftSideBar();
const variationsTab = new VariationsTab();
const examplePage = new PageBuilder().examplePage();

describe(
  'AB test variations management',
  {
    testIsolation: false,
    tags: [WebTag.web, WebTag.campaign_ab, CommonTag.experiment_detail],
  },
  function () {
    //#region Setup Test Data
    before(function () {
      cy.createAccount(Cypress.env('web_account'))
        .saveGeneratedTimeBasedIdAs('expName')
        .then(function () {
          return cy.createAPageV1(examplePage);
        })
        .then(function (response) {
          cy.wrap(response.body.id).as('testPageId');
          const experiment = new ExperimentBuilder(
            referenceData.experimentType.abTesting,
            this.expName
          )
            .setOutlierFilterEnable(false)
            .setDescription('Generated test experiment')
            .setUrl('www.optimizely.com')
            .build();
          return cy.createExperimentV1(
            experiment.layer,
            experiment.layerExperiment
          );
        });
    });
    //#endregion

    //#region Test Execution
    it('[QAK-12345][Web][Experiment Detail]_Add variation to AB experiment', function () {
      cy.visitProject();
      experimentListPage.openAnExperiment(this.expName);
      webLeftSideBar.openVariationMenu();
      variationsTab.addNewVariation('var3').verifyVariationCount(3);
    });

    it('[QAK-12346][Web][Experiment Detail]_Stop variation in AB experiment', function () {
      cy.visitProject();
      experimentListPage.openAnExperiment(this.expName);
      webLeftSideBar.openVariationMenu();
      variationsTab
        .stopAVariation('Variation #1')
        .verifyVariationTrafficAllocation('Variation #1', '0%');
    });

    it('[QAK-12347][Web][Experiment Detail]_Restore stopped variation', function () {
      cy.visitProject();
      experimentListPage.openAnExperiment(this.expName);
      webLeftSideBar.openVariationMenu();
      variationsTab
        .restoreAVariation('Variation #1')
        .verifyVariationTrafficAllocation('Variation #1', '50%');
    });
    //#endregion

    //#region Cleanup
    after(function () {
      cy.deleteAccount();
    });
    //#endregion
  }
);
