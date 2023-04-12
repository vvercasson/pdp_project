"use strict";
(self["webpackChunkauto_init"] = self["webpackChunkauto_init"] || []).push([["lib_index_js"],{

/***/ "./style/init.svg":
/*!************************!*\
  !*** ./style/init.svg ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg id=\"Layer_5\" data-name=\"Layer 5\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 343.95 340\">\n    <g xmlns=\"http://www.w3.org/2000/svg\" class=\"jp-icon3\" stroke=\"#616161\" fill=\"#616161\" fill-opacity=\"0.0\">\n        <path d=\"M260.23,106a150,150,0,1,1-87.52,28.16\" transform=\"translate(-86.27 -86)\"\n            style=\"stroke-linecap:round;stroke-miterlimit:10;stroke-width:30px\" />\n        <polyline points=\"15.5 46.29 92.69 39.53 99.44 116.72\"\n            style=\"stroke-linecap:round;stroke-linejoin:round;stroke-width:21px\" />\n        <polygon points=\"157.45 110 217.45 170 157.45 230 157.45 110\"\n            style=\"/*stroke-linejoin:round*/;stroke-width:34px\" fill-opacity=\"1.0\"/>\n    </g>\n</svg>");

/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/cells */ "webpack/sharing/consume/default/@jupyterlab/cells");
/* harmony import */ var _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _style_init_svg__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/init.svg */ "./style/init.svg");






const runInitIcon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.LabIcon({
    name: 'auto_init:init',
    svgstr: _style_init_svg__WEBPACK_IMPORTED_MODULE_5__["default"]
});
const INIT = 'init_cell';
const EXT = 'auto_init';
const MKDOWN = 'markdown';
const CODE = 'code';
const run_init_label = 'Run all cells marked as initialization';
const manualInit = (tracker) => {
    const notebook = tracker.currentWidget;
    if (notebook !== null)
        runInitCells(notebook);
};
const runInitCells = (notebook) => {
    console.log("Initializing cells");
    notebook.content.widgets.map((cell) => {
        const metadata = cell.model.metadata;
        if (metadata.get(INIT)) {
            cell.addClass(EXT + '-cell');
            switch (cell.model.type) {
                case CODE:
                    const code = cell;
                    _jupyterlab_cells__WEBPACK_IMPORTED_MODULE_3__.CodeCell.execute(code, notebook.sessionContext);
                    break;
                case MKDOWN:
                    const ce = cell;
                    ce.rendered = true;
                default:
                    break;
            }
        }
    });
};
function toggleInit(tracker) {
    let cell = tracker.activeCell;
    if (cell !== null) {
        let metadata = cell.model.metadata;
        if (metadata.get(INIT)) {
            metadata.set(INIT, false);
            cell.removeClass(EXT + '-cell');
        }
        else {
            metadata.set(INIT, true);
            cell.addClass(EXT + '-cell');
        }
        console.log(metadata.get(INIT));
    }
}
class InitManager {
    constructor() {
        this.states = new Map();
    }
    init(notebookPanel) {
        const id = notebookPanel.id;
        if (!this.states.get(id)) {
            this.states.set(id, true);
            runInitCells(notebookPanel);
        }
    }
    resetNotebook(id) {
        this.states.set(id, false);
    }
}
/**
 * Initialization data for the auto_init extension.
 */
const plugin = {
    id: 'auto_init:plugin',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker, _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_2__.IMainMenu],
    activate: (app, tracker, mainmenu) => {
        console.log('JupyterLab extension auto_init is activated!');
        const toggle_init = EXT + ':toggle_init';
        const runcommand = EXT + ':run_init';
        const manager = new InitManager();
        const runMenu = mainmenu.runMenu;
        app.commands.addCommand(toggle_init, {
            label: 'Toggle cell as initialization cell',
            execute: () => {
                toggleInit(tracker);
            }
        });
        app.commands.addCommand(runcommand, {
            label: run_init_label,
            execute: () => {
                const notebookPanel = tracker.currentWidget;
                if (notebookPanel !== null)
                    runInitCells(notebookPanel);
            }
        });
        let runAllButton = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ToolbarButton({
            actualOnClick: true,
            onClick: () => {
                manualInit(tracker);
            },
            icon: runInitIcon,
            tooltip: run_init_label
        });
        tracker.widgetAdded.connect((_, notebookPanel) => {
            const toolbar = notebookPanel.toolbar;
            notebookPanel.sessionContext.connectionStatusChanged.connect((_, status) => {
                console.log(status);
                if (status == 'connected')
                    manager.resetNotebook(notebookPanel.id);
            });
            toolbar.insertItem(10, "run_init", runAllButton);
        });
        tracker.currentChanged.connect((_, notebookPanel) => {
            if (notebookPanel !== null) {
                notebookPanel.context.ready.then(async () => {
                    return notebookPanel.sessionContext.ready;
                }).then(() => {
                    manager.init(notebookPanel);
                });
            }
        });
        console.log(tracker.selectionChanged.connect((_, panel) => {
            if (panel !== null) {
                runAllButton.enabled = true;
            }
        }));
        app.contextMenu.addItem({
            selector: '.jp-Cell',
            command: toggle_init,
            rank: 0
        });
        runMenu.addGroup([{
                command: runcommand
            }]);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.843f42ddd82ab56f4f5c.js.map