<?php

namespace App\Providers;

use Illuminate\Auth\Notifications\ResetPassword;

// use Illuminate\Support\Facades\Gate;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;

class AuthServiceProvider extends ServiceProvider
{
    /**
     * The model to policy mappings for the application.
     *
     * @var array<class-string, class-string>
     */
    protected $policies = [
        // 'App\Models\Model' => 'App\Policies\ModelPolicy',
    ];

    /**
     * Register any authentication / authorization services.
     *
     * @return void
     */
    public function boot()
    {
        $this->registerPolicies();
        $frontEndUrl = env('FRONTEND_URL');
        $this->setFrontEndUrlInResetPassword($frontEndUrl);
    }
    protected function setFrontEndUrlInResetPassword($frontEndUrl = '')
    {
        ResetPassword::createUrlUsing(function($user,string $token) use($frontEndUrl)
        {
            return $frontEndUrl . '/password/email/reset?token=' . $token;
        });
    }
}
