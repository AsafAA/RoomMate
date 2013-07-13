#import <UIKit/UIKit.h>

@interface RMWelcomeStartViewController : UIViewController

@property (weak, nonatomic) IBOutlet UITextField *nameField;
@property (weak, nonatomic) IBOutlet UIButton *nextButton;

- (IBAction)dismissKeyboard:(id)sender;
- (IBAction)nameFieldChanged:(id)sender;

@end