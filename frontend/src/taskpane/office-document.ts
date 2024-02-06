/* global Excel console */

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
      range.format.fill.color = "yellow";
      range.format.fill.pattern = "Solid";
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
}