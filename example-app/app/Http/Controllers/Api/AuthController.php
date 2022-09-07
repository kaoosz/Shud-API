<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Traits\ApiResponser;
use GrahamCampbell\ResultType\Success;
use Illuminate\Auth\Events\PasswordReset;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Password;
use Illuminate\Support\Str;
use Illuminate\Validation\ValidationException;



class AuthController extends Controller
{
    use ApiResponser;

    public function login(Request $request)
    {
        $credencials = $request->only('email','password');
       // dd($credencials);

        if(!auth()->attempt($credencials)){
            return $this->error('Credentials not match', 401);
        }
        auth()->user()->tokens()->delete();

        if(auth()->user()->is_admin){
            return $this->success([
                'user' => auth()->user(),
                'email' => auth()->user()->email,
                'token' => auth()->user()->createToken('Api Token',['server:admin'])->plainTextToken
            ]);
        }
        return $this->success([
            'user' => auth()->user()->name,
            'email' => auth()->user()->email,
            'token' => auth()->user()->createToken('API Token',['server:not'])->plainTextToken
        ]);
    }
    public function logout(Request $request)
    {
        auth()->user()->tokens()->delete();
        return[
            'message' => 'Logout and all Tokens Revoked'
        ];
    }
    public function sendPasswordResetLinkEmail(Request $request){
        $request->validate(['email' => 'required|email']);

        $status = Password::sendResetLink(
            $request->only('email')
        );

        return $status === Password::RESET_LINK_SENT
        ? $this->success(null,$message = 'Sucess Reset Password Check Your Email',200)
        : $this->error('Fail Reset Password',401);
    }

    public function resetPassword(Request $request)
    {
        $request->validate([
            'token' => 'required',
            'email' => 'required|email',
            'password' => 'required|confirmed',
        ]);

        $status = Password::reset(
            $request->only('email','password','password_confirmation','token'),
            function ($user, $password){
                $user->forceFill([
                    'password' => Hash::make($password)
                ])->setRememberToken(Str::random(60));

                $user->save();
                event(new PasswordReset($user));

            }
        );

        if($status === Password::PASSWORD_RESET){
            return response()->json(['message' => __($status)],200);
        }else{
            throw ValidationException::withMessages([
                'email fail' => __($status)
            ]);
        }
    }

}
