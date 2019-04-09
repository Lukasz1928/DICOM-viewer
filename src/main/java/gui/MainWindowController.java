package gui;

import javafx.fxml.FXML;
import javafx.scene.control.Label;

public class MainWindowController {

    @FXML
    private Label testLabel;

    @FXML
    private void initialize() {
        this.testLabel.setText("DICOM");
    }
}
