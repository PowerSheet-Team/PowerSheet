/* global Excel, Office */

const insertText = async (text: string) => {
  // Write text to the top left cell.
  try {
    await Excel.run(async (context) => {
      const sheet = context.workbook.worksheets.getActiveWorksheet();
      const range = sheet.getRange("A2");
      range.values = [[text]];
      range.format.autofitColumns();
      return context.sync();
    });
  } catch (error) {
    console.log("Error: " + error);
  }
};

export const getCellRange = async (): Promise<string> => {
  try {
    return await Excel.run(async (context) => {
      const range = context.workbook.getSelectedRange();
      // range.format.fill.color = "yellow";
      // range.format.fill.pattern = "Solid";
      range.load("address");
      await context.sync();
      return range.address;
    });
  } catch (error) {
    console.log("Error: " + error);
  }
  return null;
};

export const getRangeData = async (rangeReq: string): Promise<any[][]> => {
  try {
    return await Excel.run(async (context) => {
      const sheet = context.workbook.worksheets.getActiveWorksheet();
      const range = sheet.getRange(rangeReq);
      range.load("values");
      await context.sync();
      return range.values;
    });
  } catch (error) {
    console.log("Error: " + error);
  }
  return null;
};

export const getRangeFormula = async (rangeReq: string): Promise<any[][]> => {
  try {
    return await Excel.run(async (context) => {
      const sheet = context.workbook.worksheets.getActiveWorksheet();
      const range = sheet.getRange(rangeReq);
      range.load("formulas");
      await context.sync();
      return range.formulas;
    });
  } catch (error) {
    console.log("Error: " + error);
  }
  return null;
};

export const recvRangeCandidate = async (msg: JSON) => {
  try {
    await Excel.run(async (context) => {
      const sheet = context.workbook.worksheets.getActiveWorksheet();
      if (msg["status"] == "ok") {
        const range = sheet.getRange(msg["range"]);
        range.values = msg["candidate"];
      }
      await context.sync();
    });
  } catch (error) {
    console.log("Error: " + error);
  }
  return null;
};

export const recvCode = async (msg: JSON) => {
  try {
    await Excel.run(async (context) => {
      if (msg["status"] == "ok") {
        await hightlightSelection(msg["range"], msg["code"]);
      }
      await context.sync();
    });
  } catch (error) {
    console.log("Error: " + error);
  }
  return null;
};

export const hightlightSelection = async (area: string, stmt: string) => {
  try {
    await Excel.run(async (context) => {
      const sheet = context.workbook.worksheets.getActiveWorksheet();
      var selection = sheet.getRange(area);
      selection.load("values");
      selection.load("address");
      selection.load("rowCount");
      selection.load("columnCount");
      let cellData = [];
      let cellRaw = [];
      await context.sync();
      const values = selection.values;

      for (let i = 0; i < selection.rowCount; i++) {
        for (let j = 0; j < selection.columnCount; j++) {
          let cell = selection.getCell(i, j);
          cellRaw.push(cell);
          cell.load("address");
        }
      }
      await context.sync();

      for (let i = 0; i < selection.rowCount; i++) {
        for (let j = 0; j < selection.columnCount; j++) {
          let cell = selection.getCell(i, j);
          cellData.push({ raw: cell, value: values[i][j] });
          cell.load("address");
        }
      }
      await context.sync();
      cellData.forEach((cell) => {
        cell["address"] = cell["raw"].address;
      });

      cellData.forEach((cell) => {
        console.log(cell["value"], cell["value"] > 2);
        var value = cell["value"];
        let stmtRes = eval(stmt);
        if (stmtRes) {
          cell["raw"].format.fill.color = "yellow";
          cell["raw"].format.fill.pattern = "Solid";
        }
      });

      console.log(cellData);

      await context.sync();
    });
  } catch (error) {
    console.log("Error: " + error);
  }
  return null;
};

const promptForRangeBindingId = (): Promise<string> =>
  new Promise((resolve, reject) => {
    const handleResult = (result: Office.AsyncResult<Office.Binding>) => {
      if (result.status === Office.AsyncResultStatus.Succeeded) {
        resolve(result.value.id);
      } else {
        reject(result.error.message);
      }
    };
    Office.context.document.bindings.addFromPromptAsync(Office.BindingType.Matrix, handleResult);
  });

const getAddressesByBindingId = (bindingId: string): Promise<string> =>
  new Promise((resolve, reject) => {
    Excel.run((ctx) => {
      const binding = ctx.workbook.bindings.getItem(bindingId);
      const range = binding.getRange();
      range.load("address");
      return ctx.sync().then(() => resolve(range.address));
    })
      .catch((error) => reject(error))
      .finally(() => {
        return Office.context.document.bindings.releaseByIdAsync(bindingId);
      });
  });

const promptForAddressRange = async (): Promise<string> => {
  try {
    const bindingId = await promptForRangeBindingId();
    const address = await getAddressesByBindingId(bindingId);
    return address;
  } catch (error) {
    throw new Error(error.message);
  }
};
export { promptForAddressRange, promptForRangeBindingId, getAddressesByBindingId };
