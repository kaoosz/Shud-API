<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\CandidateController;
use App\Http\Controllers\Controller;
use App\Http\Resources\CandidateResource;
use App\Models\Candidate;
use Illuminate\Support\Str;
use Illuminate\Support\Facades\Response;



use Illuminate\Http\Request;
use Illuminate\Support\Facades\Request as FacadesRequest;

class CandidateResourceController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */

    public function index(Candidate $candidate)
    {

        $can = Candidate::query()->paginate(10);
        return CandidateResource::collection($can);

    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        //
    }

    /**
     * Display the specified resource.
     *
     * @param  \App\Models\Candidate  $candidate
     * @return \Illuminate\Http\Response
     */
    public function test(){
        return 'fun';
    }
    public function show(Candidate $candidate,Request $request)
    {
        if(request()->get('csv')){
            $ApiPython = $request->fullUrl();
            //$two = "http://142.93.244.160/api/candidatos/candidatos?urna=MARCELO ARO&NR_CANDIDATO=3133&ANO=2018&bairro=bairro2018&csv=csv";
            $code = base64_encode($ApiPython);

            if($request->has('paginate')){
                return 'Remove Paginate To Create Csv';
            }
            //$comando = exec("python3 /home/guilherme/Development/Shud-API/example-app/public/Gerador.py {$code}");

            //var_dump($comando);

            // $file = public_path()."/outpu.csv";
            // $headers = array(
            //     'Content-Type: application/pdf',
            // );
            // return Response::download($file, 'outpu.csv', $headers);

            return 'Sucess Csv';
               
        }

        if(!request()->get('ANO') or !request()->get('NR_CANDIDATO') ){
            $can = Candidate::query()
            ->where('NM_URNA_CANDIDATO',request()->get('urna'))->paginate(10);
        }

        if(request()->get('ANO')){

            $can = Candidate::query()
            ->when(request()->get('escola') === 'schools2020',fn($query) => $query->with('schools2020'))
            ->when(request()->get('escola') === 'schools2018',fn($query) => $query->with('schools2018'))
            ->when(request()->get('escola') === 'schools2016',fn($query) => $query->with('schools2016'))
            ->when(request()->get('escola') === 'schools2014',fn($query) => $query->with('schools2014'))
            ->when(request()->get('escola') === 'schools2012',fn($query) => $query->with('schools2012'))

            ->when(request()->get('cidade') === 'cities2020',fn($query) => $query->with('cities2020'))
            ->when(request()->get('cidade') === 'cities2018',fn($query) => $query->with('cities2018'))
            ->when(request()->get('cidade') === 'cities2016',fn($query) => $query->with('cities2016'))
            ->when(request()->get('cidade') === 'cities2014',fn($query) => $query->with('cities2014'))
            ->when(request()->get('cidade') === 'cities2012',fn($query) => $query->with('cities2012'))

            ->when(request()->get('bairro') === 'bairro2020',fn($query) => $query->with('bairro2020'))
            ->when(request()->get('bairro') === 'bairro2018',fn($query) => $query->with('bairro2018'))
            ->when(request()->get('bairro') === 'bairro2016',fn($query) => $query->with('bairro2016'))
            ->when(request()->get('bairro') === 'bairro2014',fn($query) => $query->with('bairro2014'))
            ->when(request()->get('bairro') === 'bairro2012',fn($query) => $query->with('bairro2012'))

            ->where([['NM_URNA_CANDIDATO',request()->get('urna')],
            ['ANO_ELEICAO',request()->get('ANO')],
            ['NR_CANDIDATO',request()->get('NR_CANDIDATO')]]
            )->get();

            //return CandidateResource::collection($can);
        }

        return CandidateResource::collection($can);

    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  \App\Models\Candidate  $candidate
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, Candidate $candidate)
    {
        //
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  \App\Models\Candidate  $candidate
     * @return \Illuminate\Http\Response
     */
    public function destroy(Candidate $candidate)
    {
        //
    }
}
