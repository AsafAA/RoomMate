#import <UIKit/UIKit.h>

@interface RMSettingsViewController : UITableViewController

@property (weak, nonatomic) IBOutlet UITextField *nameField;

- (IBAction)done:(id)sender;
- (IBAction)dismissKeyboard:(id)sender;

@end