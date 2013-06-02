<?php

class my404 extends CI_Controller {

    public function __construct() {
        parent::__construct();
    }

    public function index() {
        $this->output->set_status_header('404');
        $data['title'] = 'Page not found';
        $this->load->view('templates/header', $data); //loading in my template
        $this->load->view('404'); //loading in my template
        $this->load->view('templates/footer'); //loading in my template
    }

}
