# PPT alignment

The supplied *PADDY LEAVES PPT-1.pdf* was used as a requirements reference. The implementation covers leaf-image acquisition, preprocessing/leaf masking, CNN multi-class prediction, visible-damage severity estimation, pesticide/fertilizer guidance, and a local prediction-history store.

The PPT requests treatment measurements by severity. This application intentionally does **not** generate pesticide quantities: valid rates depend on the country, registered product, crop stage, water conditions, and label. It instead directs users to locally registered products and their labels.

## Data and model boundary

The externally sourced UCI dataset has only three labeled classes: bacterial leaf blight, brown spot, and leaf smut. The model predicts only those classes. Other diseases listed in the knowledge base are reference-only until sufficiently licensed, labeled images are added and a new model is trained.
