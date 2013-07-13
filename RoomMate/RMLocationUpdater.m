#import "RMLocationUpdater.h"
#import "RMAPI.h"

@interface RMLocationUpdater ()

@property (strong) CLLocationManager *locationManager;

@end

@implementation RMLocationUpdater

+ (RMLocationUpdater *)sharedUpdater {
    static RMLocationUpdater *sharedUpdater = nil;
    
    if (sharedUpdater == nil) {
        sharedUpdater = [[RMLocationUpdater alloc] init];
    }
    
    return sharedUpdater;
}

- (id)init {
    self = [super init];
    
    if (self) {
        self.locationManager = [[CLLocationManager alloc] init];
        self.locationManager.delegate = self;
    }
    
    return self;
}

- (void)start {
    [self.locationManager startUpdatingLocation];
}

- (void)locationManager:(CLLocationManager *)manager didUpdateLocations:(NSArray *)locations {
    CLLocation *location = [locations lastObject];
    [RMAPI updateLocation:location];
}

@end